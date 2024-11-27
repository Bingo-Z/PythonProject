import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from email.header import decode_header
import openai
from googletrans import Translator
import sqlite3
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class EmailProcessor:
    def __init__(self):
        # 邮箱配置
        self.EMAIL = os.getenv('EMAIL')
        self.PASSWORD = os.getenv('EMAIL_PASSWORD')
        self.IMAP_SERVER = os.getenv('IMAP_SERVER')
        self.SMTP_SERVER = os.getenv('SMTP_SERVER')  # 添加SMTP服务器配置
        self.SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))  # 添加SMTP端口配置
        
        # OpenAI配置
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # 翻译器初始化
        self.translator = Translator()
        
        # 数据库连接
        self.conn = sqlite3.connect('email_processing.db')
        self.create_tables()
        
    def create_tables(self):
        """创建必要的数据库表"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT UNIQUE,
            subject TEXT,
            original_content TEXT,
            translated_content TEXT,
            outline TEXT,
            processed_date TIMESTAMP
        )
        ''')
        self.conn.commit()

    def connect_to_email(self):
        """连接到邮件服务器"""
        try:
            mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            mail.login(self.EMAIL, self.PASSWORD)
            return mail
        except Exception as e:
            print(f"邮件服务器连接失败: {e}")
            return None

    def get_email_content(self, mail):
        """获取邮件内容"""
        mail.select('INBOX')
        _, messages = mail.search(None, 'UNSEEN')  # 获取未读邮件
        
        for num in messages[0].split():
            try:
                _, msg_data = mail.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                subject = self.decode_email_header(email_message['subject'])
                content = self.get_email_body(email_message)
                
                if content:
                    self.process_email(email_message['message-id'], subject, content)
                
            except Exception as e:
                print(f"处理邮件失败: {e}")

    def decode_email_header(self, header):
        """解码邮件标题"""
        decoded_header = decode_header(header)[0]
        if decoded_header[1]:
            return decoded_header[0].decode(decoded_header[1])
        return decoded_header[0]

    def get_email_body(self, email_message):
        """提取邮件正文"""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()

    def translate_content(self, content):
        """翻译内容"""
        try:
            translated = self.translator.translate(content, dest='zh-cn')
            return translated.text
        except Exception as e:
            print(f"翻译失败: {e}")
            return content

    def generate_outline(self, content):
        """使用AI生成大纲"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "请为以下内容生成一个结构化的大纲。"},
                    {"role": "user", "content": content}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI处理失败: {e}")
            return "AI处理失败"

    def save_to_database(self, email_id, subject, original_content, 
                        translated_content, outline):
        """保存处理结果到数据库"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO processed_emails 
        (email_id, subject, original_content, translated_content, outline, processed_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (email_id, subject, original_content, translated_content, 
              outline, datetime.now()))
        self.conn.commit()

    def send_processed_email(self, original_subject, translated_content, outline):
        """发送处理结果邮件"""
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.EMAIL
            msg['To'] = self.EMAIL
            msg['Subject'] = f"处理结果: {original_subject}"

            # 构建邮件正文
            email_body = f"""
            原始邮件主题: {original_subject}
            
            翻译结果:
            {'-' * 50}
            {translated_content}
            
            内容大纲:
            {'-' * 50}
            {outline}
            """

            msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

            # 连接SMTP服务器并发送
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()  # 启用TLS加密
                server.login(self.EMAIL, self.PASSWORD)
                server.send_message(msg)
                
            print(f"处理结果已发送: {original_subject}")
            return True
            
        except Exception as e:
            print(f"发送处理结果失败: {e}")
            return False

    def process_email(self, email_id, subject, content):
        """处理单个邮件"""
        # 翻译内容
        translated_content = self.translate_content(content)
        
        # 生成大纲
        outline = self.generate_outline(translated_content)
        
        # 保存结果
        self.save_to_database(email_id, subject, content, 
                            translated_content, outline)
        
        # 发送处理结果
        self.send_processed_email(subject, translated_content, outline)

    def run(self):
        """主运行循环"""
        while True:
            try:
                mail = self.connect_to_email()
                if mail:
                    self.get_email_content(mail)
                    mail.logout()
                
                time.sleep(300)  # 每5分钟检查一次
                
            except Exception as e:
                print(f"运行错误: {e}")
                time.sleep(60)  # 发生错误时等待1分钟后重试 