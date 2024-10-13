import cv2
import os


# 导入所需的库
# cv2 用于图像处理
# os 用于文件和目录操作

def read_images_from_folder(folder_path):
    """
    从指定文件夹读取图片文件
    :param folder_path: 图片所在文件夹的路径
    :return: 包含(文件名, 图像数据)元组的列表
    """
    images = []
    for file in os.listdir(folder_path):
        # 检查文件是否为支持的图片格式
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(folder_path, file)
            img = cv2.imread(img_path)
            if img is not None:
                images.append((file, img))
                print(f"成功读取图片: {file}")
            else:
                print(f"无法读取图片: {file}")
    return images


def save_images_to_folder(images, output_folder):
    """
    将图片保存到指定文件夹
    :param images: 包含(文件名, 图像数据)元组的列表
    :param output_folder: 输出文件夹的路径
    """
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出文件夹: {output_folder}")

    # 遍历图片列表，将每张图片保存到输出文件夹
    for file_name, img in images:
        output_path = os.path.join(output_folder, file_name)
        cv2.imwrite(output_path, img)
        print(f"保存图片: {file_name} 到 {output_path}")
