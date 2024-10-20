from PyQt5.QtWidgets import QApplication

from utils.dataLoad import read_images_from_folder, save_images_to_folder
from utils.ui import ImageProcessorGUI


#
# def main():
#     """
#     主函数，用于演示如何使用read_images_from_folder和save_images_to_folder函数
#     """
#     # 定义输入和输出文件夹路径
#     input_folder = "path/to/input/folder"
#     output_folder = "path/to/output/folder"
#
#     print("开始处理图片...")
#
#     # 从输入文件夹读取图片
#     images = read_images_from_folder(input_folder)
#     print(f"共读取 {len(images)} 张图片")
#
#     # 将图片保存到输出文件夹
#     save_images_to_folder(images, output_folder)
#
#     print("图片处理完成！")
def main():
    app = QApplication([])  # 创建QApplication实例
    window = ImageProcessorGUI()  # 创建主窗口实例
    window.show()  # 显示主窗口
    app.exec_()  # 进入应用程序的主循环
# 如果这个脚本是作为主程序运行的，则执行main函数
if __name__ == "__main__":
    main()