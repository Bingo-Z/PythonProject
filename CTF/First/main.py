import os

from license_manager import LicenseManager
from exe_protector import protect_exe


def main():
    # 初始化许可证管理器
    license_manager = LicenseManager()

    while True:
        print("\n1. 生成卡密")
        print("2. 保护exe文件")
        print("3. 退出")

        choice = input("请选择操作: ")

        if choice == "1":
            days = int(input("请输入卡密有效期(天数): "))
            license_key = license_manager.generate_license(days)
            print(f"生成的卡密: {license_key}")

        elif choice == "2":
            original_exe = input("请输入要保护的exe文件路径: ")
            output_path = input("请输入输出目录路径: ")

            if not os.path.exists(original_exe):
                print("找不到指定的exe文件")
                continue

            protect_exe(original_exe, output_path)
            print("exe文件保护完成")

        elif choice == "3":
            break

        else:
            print("无效的选择")


if __name__ == "__main__":
    main()