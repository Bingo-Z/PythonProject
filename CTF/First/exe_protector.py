import os
import shutil
import tempfile
import sys
import subprocess
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import ctypes
import glob


def encrypt_exe_and_dlls(exe_path, key):
    """加密exe文件和相关的DLL文件"""
    # 获取exe所在目录
    exe_dir = os.path.dirname(exe_path)
    exe_name = os.path.basename(exe_path)

    # 收集所有需要加密的文件
    files_to_encrypt = {}

    # 添加主程序
    with open(exe_path, 'rb') as f:
        files_to_encrypt[exe_name] = f.read()

    # 添加同目录下的所有DLL文件
    for dll_file in glob.glob(os.path.join(exe_dir, "*.dll")):
        dll_name = os.path.basename(dll_file)
        with open(dll_file, 'rb') as f:
            files_to_encrypt[dll_name] = f.read()

    # 加密所有文件
    encrypted_files = {}
    for filename, data in files_to_encrypt.items():
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        encrypted_files[filename] = {
            'nonce': nonce,
            'tag': tag,
            'ciphertext': ciphertext
        }

    return encrypted_files


def protect_exe(original_exe_path, output_exe_path):
    """给exe文件添加卡密保护"""
    verification_code = '''
from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import messagebox
import sys
import os
import json
from datetime import datetime
import subprocess
import tempfile

def decrypt_license(encrypted_license, key):
    """解密卡密数据"""
    try:
        original_key, encrypted_data = encrypted_license.split('.')
        raw_data = base64.b64decode(encrypted_data)
        nonce = raw_data[:16]
        tag = raw_data[16:32]
        ciphertext = raw_data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        license_data = json.loads(data.decode('utf-8'))
        if license_data['key'] != original_key:
            return None
        return license_data
    except Exception:
        return None

def decrypt_and_run_exe(encrypted_dir, key):
    """解密并运行exe文件及其DLL"""
    try:
        temp_dir = tempfile.mkdtemp()

        # 读取并解密所有文件
        for filename in os.listdir(encrypted_dir):
            if filename.endswith('.encrypted'):
                original_name = filename[:-10]  # 移除.encrypted后缀
                encrypted_path = os.path.join(encrypted_dir, filename)

                with open(encrypted_path, 'rb') as f:
                    nonce = f.read(16)
                    tag = f.read(16)
                    ciphertext = f.read()

                # 解密
                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                file_data = cipher.decrypt_and_verify(ciphertext, tag)

                # 保存解密后的文件
                output_path = os.path.join(temp_dir, original_name)
                with open(output_path, 'wb') as f:
                    f.write(file_data)

        # 查找主程序exe
        exe_files = [f for f in os.listdir(temp_dir) if f.endswith('.exe')]
        if not exe_files:
            raise Exception("找不到主程序文件")

        main_exe = os.path.join(temp_dir, exe_files[0])

        # 运行程序
        subprocess.run([main_exe], cwd=temp_dir)

        # 清理临时文件
        shutil.rmtree(temp_dir)

    except Exception as e:
        messagebox.showerror("错误", f"程序运行失败: {str(e)}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def verify_license():
    """验证卡密"""
    encrypted_license = entry.get()
    key = b'1234567890123456'

    if not encrypted_license:
        messagebox.showerror("错误", "请输入卡密")
        return

    # 解密并验证卡密
    license_data = decrypt_license(encrypted_license, key)

    if not license_data:
        messagebox.showerror("错误", "无效的卡密")
        return

    # 检查卡密是否过期
    if datetime.now().timestamp() > license_data["expiry_date"]:
        messagebox.showerror("错误", "卡密已过期")
        return

    # 检查卡密是否已使用
    if license_data["is_used"]:
        messagebox.showerror("错误", "卡密已被使用")
        return

    # 验证成功后的部分改为：
    try:
        root.withdraw()

        # 获取加密文件所在目录
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # 解密并运行
        decrypt_and_run_exe(current_dir, key)
        os._exit(0)

    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {str(e)}")
        root.deiconify()

# 创建验证窗口
root = tk.Tk()
root.title("卡密验证")
root.geometry("400x180")
root.resizable(False, False)
root.attributes('-topmost', True)

# 窗口居中
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 400) // 2
y = (screen_height - 180) // 2
root.geometry(f"400x180+{x}+{y}")

label = tk.Label(root, text="请输入卡密:", font=("Arial", 12))
label.pack(pady=20)

entry = tk.Entry(root, width=50, font=("Arial", 10))
entry.pack()

verify_button = tk.Button(root, text="验证", command=verify_license, 
                         width=10, height=1, font=("Arial", 10))
verify_button.pack(pady=20)

root.bind('<Return>', lambda event: verify_license())
root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

root.mainloop()
'''

    # 创建临时目录
    temp_dir = tempfile.mkdtemp()

    try:
        # 加密exe和DLL文件
        key = b'1234567890123456'
        encrypted_files = encrypt_exe_and_dlls(original_exe_path, key)

        # 保存加密后的文件
        for filename, encrypted_data in encrypted_files.items():
            encrypted_path = os.path.join(output_exe_path, f"{filename}.encrypted")
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data['nonce'])
                f.write(encrypted_data['tag'])
                f.write(encrypted_data['ciphertext'])

        # 创建验证程序
        verifier_path = os.path.join(temp_dir, "verifier.py")
        with open(verifier_path, "w", encoding="utf-8") as f:
            f.write(verification_code)

        # 创建spec文件
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{verifier_path}'],
    pathex=[r'{temp_dir}'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='verifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
'''

        spec_path = os.path.join(temp_dir, "verifier.spec")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)

        # 使用PyInstaller打包验证程序
        python_exe = sys.executable
        pyinstaller_args = [
            python_exe,
            '-m',
            'PyInstaller',
            '--clean',
            '--distpath',
            output_exe_path,
            spec_path
        ]

        process = subprocess.Popen(
            pyinstaller_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            cwd=temp_dir
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error_msg = f"PyInstaller打包失败:\n{stderr}"
            raise Exception(error_msg)

        # 检查输出文件
        verifier_exe = os.path.join(output_exe_path, "verifier.exe")
        if not os.path.exists(verifier_exe):
            raise Exception("打包后的文件未找到")

    except Exception as e:
        raise Exception(f"保护过程出错: {str(e)}")

    finally:
        # 清理临时文件
        try:
            shutil.rmtree(temp_dir)
        except:
            pass