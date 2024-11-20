# -*- coding: utf-8 -*-
import cv2
import os
import glob

def draw_boxes_on_image(image_path, annotations_path, classes_path, output_folder):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像文件: {image_path}")
        return

    # 读取类别信息
    with open(classes_path, 'r', encoding='utf-8') as f:
        classes = f.readlines()
    classes = [cls.strip() for cls in classes]

    # 读取标注信息
    with open(annotations_path, 'r', encoding='utf-8') as f:
        annotations = f.readlines()

    # 获取图像的宽度和高度
    height, width, _ = image.shape

    # 绘制标注框
    for annotation in annotations:
        # 解析坐标
        parts = list(map(float, annotation.strip().split()))
        class_index = int(parts[0])
        x_center = parts[1]
        y_center = parts[2]
        box_width = parts[3]
        box_height = parts[4]

        # 计算绝对坐标
        x_min = int((x_center - box_width / 2) * width)
        y_min = int((y_center - box_height / 2) * height)
        x_max = int((x_center + box_width / 2) * width)
        y_max = int((y_center + box_height / 2) * height)

        # 绘制矩形框
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # 绿色框
        # 在框上方添加类别标签
        label = classes[class_index] if class_index < len(classes) else "Unknown"
        cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 保存标注后的图像
    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_image_path, image)
    print(f"保存标注后的图像: {output_image_path}")

    # 显示图像
    cv2.imshow("Annotated Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_images_in_folder(images_folder, annotations_folder, classes_path, output_folder):
    # 获取所有图像文件
    image_files = glob.glob(os.path.join(images_folder, "*.jpg"))  # 假设是jpg格式
    for image_path in image_files:
        # 构建对应的标注文件路径
        annotation_file = os.path.join(annotations_folder, os.path.basename(image_path).replace('.jpg', '.txt'))
        if os.path.exists(annotation_file):
            draw_boxes_on_image(image_path, annotation_file, classes_path, output_folder)
        else:
            print(f"未找到标注文件: {annotation_file}")

if __name__ == "__main__":
    images_folder = r"D:/Bingo/openCV/data/test/images"  # 替换为你的图片文件夹路径
    annotations_folder = r"D:/Bingo/openCV/data/test/labels"  # 替换为你的标注文件夹路径
    classes_path = r"D:/Bingo/openCV/data/test/labels/classes.txt"  # 替换为你的类别文件路径
    output_folder = r"D:/Bingo/openCV/data/output"  # 替换为你的输出文件夹路径
    os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在
    process_images_in_folder(images_folder, annotations_folder, classes_path, output_folder)