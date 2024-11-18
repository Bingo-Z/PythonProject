from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from license_manager import LicenseManager
from exe_protector import protect_exe
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.license_manager = LicenseManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EXE文件加密工具')
        self.setFixedSize(600, 500)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # 设置统一的字体
        default_font = QFont()
        default_font.setPointSize(10)

        # 卡密生成部分
        title1 = QLabel('生成卡密')
        title1.setStyleSheet('font-size: 18px; font-weight: bold; color: #2c3e50;')
        title1.setFixedHeight(40)
        layout.addWidget(title1)

        self.days_input = QLineEdit()
        self.days_input.setFont(default_font)
        self.days_input.setPlaceholderText('请输入卡密有效期(天数)')
        self.days_input.setFixedHeight(35)
        self.days_input.setStyleSheet('''
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        ''')
        layout.addWidget(self.days_input)

        generate_btn = QPushButton('生成卡密')
        generate_btn.setFont(default_font)
        generate_btn.setFixedHeight(35)
        generate_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        generate_btn.clicked.connect(self.generate_license)
        layout.addWidget(generate_btn)

        # 创建水平布局来放置卡密显示框和复制按钮
        license_layout = QHBoxLayout()

        self.license_display = QLineEdit()
        self.license_display.setFont(default_font)
        self.license_display.setReadOnly(True)
        self.license_display.setPlaceholderText('生成的卡密将显示在这里')
        self.license_display.setFixedHeight(35)
        self.license_display.setStyleSheet('''
            QLineEdit {
                padding: 5px 10px;
                background-color: #f5f6fa;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
        ''')
        license_layout.addWidget(self.license_display)

        # 添加复制按钮
        copy_btn = QPushButton('复制卡密')
        copy_btn.setFont(default_font)
        copy_btn.setFixedHeight(35)
        copy_btn.setFixedWidth(80)
        copy_btn.setStyleSheet('''
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        ''')
        copy_btn.clicked.connect(self.copy_license)
        license_layout.addWidget(copy_btn)

        # 将水平布局添加到主布局
        layout.addLayout(license_layout)

        # 分隔线
        line = QLabel()
        line.setStyleSheet('background-color: #bdc3c7;')
        line.setFixedHeight(2)
        layout.addWidget(line)

        # EXE保护部分
        title2 = QLabel('保护EXE文件')
        title2.setStyleSheet('font-size: 18px; font-weight: bold; color: #2c3e50;')
        title2.setFixedHeight(40)
        layout.addWidget(title2)

        # 文件路径显示和选择按钮水平布局
        self.exe_path_input = QLineEdit()
        self.exe_path_input.setFont(default_font)
        self.exe_path_input.setPlaceholderText('选择要保护的EXE文件')
        self.exe_path_input.setFixedHeight(35)
        self.exe_path_input.setStyleSheet('''
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
        ''')
        layout.addWidget(self.exe_path_input)

        select_exe_btn = QPushButton('选择EXE文件')
        select_exe_btn.setFont(default_font)
        select_exe_btn.setFixedHeight(35)
        select_exe_btn.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        select_exe_btn.clicked.connect(self.select_exe)
        layout.addWidget(select_exe_btn)

        self.output_path_input = QLineEdit()
        self.output_path_input.setFont(default_font)
        self.output_path_input.setPlaceholderText('选择输出目录')
        self.output_path_input.setFixedHeight(35)
        self.output_path_input.setStyleSheet('''
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
        ''')
        layout.addWidget(self.output_path_input)

        select_output_btn = QPushButton('选择输出目录')
        select_output_btn.setFont(default_font)
        select_output_btn.setFixedHeight(35)
        select_output_btn.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        select_output_btn.clicked.connect(self.select_output)
        layout.addWidget(select_output_btn)

        protect_btn = QPushButton('开始保护')
        protect_btn.setFont(default_font)
        protect_btn.setFixedHeight(40)
        protect_btn.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        protect_btn.clicked.connect(self.protect_exe_file)
        layout.addWidget(protect_btn)

    def generate_license(self):
        """生成卡密"""
        days_text = self.days_input.text().strip()  # 去除空白字符

        # 检查是否为空
        if not days_text:
            QMessageBox.warning(self, '警告', '请输入卡密有效期')
            return

        # 检查是否只包含数字
        if not all(c.isdigit() for c in days_text):
            QMessageBox.warning(self, '警告', '请只输入纯数字，不要包含其他字符')
            self.days_input.clear()
            return

        # 转换为数字并验证范围
        days = int(days_text)
        if days <= 0:
            QMessageBox.warning(self, '警告', '天数必须大于0')
            self.days_input.clear()
            return
        elif days > 3650:  # 10年限制
            QMessageBox.warning(self, '警告', '天数不能超过3650天')
            self.days_input.clear()
            return

        # 生成卡密
        try:
            license_key = self.license_manager.generate_license(days)
            self.license_display.setText(license_key)
            self.days_input.clear()  # 清空输入框
            QMessageBox.information(self, '成功', f'已生成{days}天的卡密')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成卡密失败：{str(e)}')
            self.days_input.clear()

    def select_exe(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择EXE文件",
            "",
            "EXE文件 (*.exe)"
        )
        if file_path:
            self.exe_path_input.setText(file_path)

    def select_output(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            ""
        )
        if dir_path:
            self.output_path_input.setText(dir_path)

    def protect_exe_file(self):
        exe_path = self.exe_path_input.text()
        output_path = self.output_path_input.text()

        if not exe_path or not output_path:
            QMessageBox.warning(self, '警告', '请选择EXE文件和输出目录')
            return

        if not os.path.exists(exe_path):
            QMessageBox.warning(self, '警告', '选择的EXE文件不存在')
            return

        try:
            protect_exe(exe_path, output_path)
            QMessageBox.information(self, '成功', 'EXE文件保护完成')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保护过程出错：{str(e)}')

    def copy_license(self):
        """复制卡密到剪贴板"""
        license_key = self.license_display.text()
        if license_key:
            clipboard = QApplication.clipboard()
            clipboard.setText(license_key)
            # 显示提示
            QMessageBox.information(self, '成功', '卡密已复制到剪贴板')
        else:
            QMessageBox.warning(self, '警告', '请先生成卡密')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()