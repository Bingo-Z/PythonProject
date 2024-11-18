import random
import string
import json
import os
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


class LicenseManager:
    def __init__(self):
        self.key = b'1234567890123456'  # 16字节密钥

    def generate_license(self, days=30):
        """生成新的卡密"""
        # 生成基础卡密
        license_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        expiry_date = (datetime.now().timestamp() + days * 24 * 3600)

        # 创建许可证数据
        license_data = {
            "key": license_key,
            "expiry_date": expiry_date,
            "is_used": False
        }

        # 加密许可证数据
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        json_str = json.dumps(license_data)
        ciphertext, tag = cipher.encrypt_and_digest(json_str.encode('utf-8'))

        # 将nonce, tag和密文组合并base64编码
        encrypted_data = base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

        # 返回完整的卡密（原始卡密 + 加密数据）
        return f"{license_key}.{encrypted_data}"

    def verify_license(self, license_key):
        """验证卡密是否有效"""
        if license_key not in self.licenses:
            return False, "无效的卡密"

        license_data = self.licenses[license_key]
        if license_data["is_used"]:
            return False, "卡密已被使用"

        if datetime.now().timestamp() > license_data["expiry_date"]:
            return False, "卡密已过期"

        return True, "卡密验证成功"

    def _encrypt_data(self, data):
        """加密数据"""
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        json_str = json.dumps(data)
        ciphertext, tag = cipher.encrypt_and_digest(json_str.encode('utf-8'))

        # 将nonce, tag和密文组合并base64编码
        encrypted_data = base64.b64encode(nonce + tag + ciphertext).decode('utf-8')
        return encrypted_data

    def _decrypt_data(self, encrypted_data):
        """解密数据"""
        try:
            # base64解码
            raw_data = base64.b64decode(encrypted_data)

            # 提取nonce, tag和密文
            nonce = raw_data[:16]
            tag = raw_data[16:32]
            ciphertext = raw_data[32:]

            # 解密
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)

            return json.loads(data.decode('utf-8'))
        except Exception:
            return {}

    def _load_licenses(self):
        """从加密文件加载卡密数据"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    encrypted_data = f.read()
                return self._decrypt_data(encrypted_data)
            except Exception:
                return {}
        return {}

    def _save_licenses(self):
        """保存加密的卡密数据到文件"""
        encrypted_data = self._encrypt_data(self.licenses)
        with open(self.license_file, 'w') as f:
            f.write(encrypted_data)