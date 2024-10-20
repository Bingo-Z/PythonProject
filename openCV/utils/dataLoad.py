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

def read_matching_text(image_name, txt_file_path):
    """
    读取与图片名字相同的txt文件内容
    :param image_name: 图片文件名（不包含路径）
    :param txt_file_path: txt文件的完整路径
    :return: 包含txt文件内容的data列表，如果文件不存在或读取失败则返回空列表
    """
    # 获取图片的文件名（不含扩展名）
    image_base_name = os.path.splitext(image_name)[0]

    # 获取txt文件的文件名（不含扩展名）
    txt_base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    data2 = []
    # 检查文件名是否匹配

    if not os.path.exists(txt_base_name):
        return data2
    if os.path.getsize(txt_base_name) == 0:
        return data2
    if image_base_name == txt_base_name:
        try:
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                # 读取文件内容并按行分割
                lines = txt_file.readlines()
                # 去除每行的首尾空白字符并过滤掉空行
                data = [line.strip() for line in lines if line.strip()]
                data2.append([float(i) for i in data])
                return data
        except Exception as e:
            print(f"读取文本文件时出错: {txt_file_path}. 错误: {str(e)}")
    else:
        print(f"图片文件名 {image_name} 与文本文件名 {txt_file_path} 不匹配")

    return data2


def save_image_and_boxes(img, boxes, save_path, prefix, image_name):
    """
    将图片和对应的边界框信息保存到指定文件夹
    :param img: 图像数据（numpy数组）
    :param boxes: 包含边界框信息的列表
    :param save_path: 输出文件夹的路径
    :param prefix: 文件名前缀
    :param image_name: 原始图片文件名
    """
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"创建输出文件夹: {save_path}")

    # 生成新的文件名
    base_name = os.path.splitext(image_name)[0]
    new_image_name = f"{prefix}{base_name}.jpg"
    new_txt_name = f"{prefix}{base_name}.txt"

    # 保存图片
    image_path = os.path.join(save_path, new_image_name)
    cv2.imwrite(image_path, img)
    print(f"保存图片: {new_image_name} 到 {image_path}")

    # 保存边界框信息
    txt_path = os.path.join(save_path, new_txt_name)
    with open(txt_path, 'w', encoding='utf-8') as f:
        for box in boxes:
            f.write(f"{box}\n")
    print(f"保存边界框信息: {new_txt_name} 到 {txt_path}")


def display_image_with_boxes(img, boxes):
    """
    在图像上显示边界框
    :param img: 图像数据（numpy数组）
    :param boxes: 包含边界框信息的列表
    :return: 带有边界框的图像
    """
    img_with_boxes = img.copy()
    height, width = img.shape[:2]

    for box in boxes:
        # 假设box格式为：class x_center y_center width height
        parts = box.split()
        if len(parts) == 5:
            cls, x_center, y_center, w, h = parts
            x_center, y_center, w, h = map(float, [x_center, y_center, w, h])

            # 将相对坐标转换为绝对坐标
            x1 = int((x_center - w / 2) * width)
            y1 = int((y_center - h / 2) * height)
            x2 = int((x_center + w / 2) * width)
            y2 = int((y_center + h / 2) * height)

            # 绘制边界框
            cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 添加类别标签
            cv2.putText(img_with_boxes, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return img_with_boxes