import cv2
import numpy as np
import matplotlib.pyplot as plt

from dataLoad import read_images_from_folder, save_image_and_boxes


def random_contrast(image, alpha_range=(0.5, 2.0)):
    alpha = np.random.uniform(*alpha_range)  # 随机选择对比度因子
    return cv2.convertScaleAbs(image, alpha=alpha)

def main():
    # 加载图像
    image = cv2.imread('E:/PythonProject/openCV/data/test/images/1.jpg')

    # 应用三种不同的随机对比度增强
    contrast1 = random_contrast(image)
    contrast2 = random_contrast(image)
    contrast3 = random_contrast(image)

    # 展示结果
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 4, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.title('Contrast 1')
    plt.imshow(cv2.cvtColor(contrast1, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.title('Contrast 2')
    plt.imshow(cv2.cvtColor(contrast2, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.title('Contrast 3')
    plt.imshow(cv2.cvtColor(contrast3, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.show()


    folder_path = 'E:/PythonProject/openCV/data/test/images'  # 图像文件夹路径
    save_path = 'E:/PythonProject/openCV/data/3'  # 保存增强图像的路径
    prefix = 'augmented_'  # 文件名前缀

    images = read_images_from_folder(folder_path)
    i=0
    for image_name, img in images:
        # 应用三种不同的随机对比度增强
        contrast1 = random_contrast(img)
        contrast2 = random_contrast(img)
        contrast3 = random_contrast(img)

        # 保存增强后的图像和边界框信息（假设 boxes 是已定义的边界框列表）
        boxes = []  # 这里需要定义边界框信息
        save_image_and_boxes(contrast1, boxes, save_path, prefix, f'color_image_{i+1}.jpg')
        save_image_and_boxes(contrast2, boxes, save_path, prefix, f'color_image_{i+2}.jpg')
        save_image_and_boxes(contrast3, boxes, save_path, prefix, f'color_image_{i+3}.jpg')
if __name__ == "__main__":
    main()