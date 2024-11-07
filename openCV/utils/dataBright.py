import cv2
import numpy as np
import random

from dataLoad import save_image_and_boxes


def random_brightness(image):
    # 随机选择亮度因子
    factor = random.uniform(0.5, 1.5)  # 亮度因子范围
    # 调整图像亮度
    bright_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)
    return bright_image


def random_color_transform(image):
    # 随机选择色彩变换因子
    factors = [random.uniform(0.5, 1.5) for _ in range(3)]  # 随机生成3个因子
    b_factor, g_factor, r_factor = factors  # 蓝色、绿色、红色通道因子

    # 分离通道
    b, g, r = cv2.split(image)

    # 应用变换
    #通过调整每个颜色通道的亮度因子alpha，来实现对图像的色彩变换
    #固定为 1.0，即不进行亮度调整
    b = cv2.convertScaleAbs(b, alpha=b_factor, beta=0)
    g = cv2.convertScaleAbs(g, alpha=g_factor, beta=0)
    r = cv2.convertScaleAbs(r, alpha=r_factor, beta=0)

    # 合并通道
    transformed_image = cv2.merge((b, g, r))
    return transformed_image

def random_color_transform(image):
    # 随机选择颜色变换因子
    factors = [random.uniform(0.5, 1.5) for _ in range(3)]  # 对于B、G、R通道
    # 调整图像颜色
    color_image = cv2.merge([cv2.convertScaleAbs(image[:, :, i], alpha=factors[i], beta=0) for i in range(3)])
    return color_image

# 示例用法
image = cv2.imread('E:/PythonProject/openCV/data/test/images/1.jpg')
# ... existing code ...
color_images = [random_color_transform(image) for _ in range(5)]  # 生成5种随机颜色变换的图像

# 显示结果
# ... existing code ...

for i, color_image in enumerate(color_images):
    cv2.imshow(f'Color Transformed Image {i+1}', color_image)
    # 添加等待键盘输入以终止循环
    if cv2.waitKey(0) & 0xFF == ord('q'):  # 按 'q' 键退出
        break
# ... existing code ...
# 保存颜色变换后的图像和边界框信息
boxes = []  # 假设这里有边界框信息
save_path = 'E:/PythonProject/openCV/data/2'  # 指定保存路径
prefix = 'color_transformed_'  # 文件名前缀
for i, color_image in enumerate(color_images):
    save_image_and_boxes(color_image, boxes, save_path, prefix, f'color_image_{i+1}.jpg')
"""

# 示例用法
image = cv2.imread('E:/PythonProject/openCV/data/test/images/1.jpg')
bright_image = random_brightness(image)
# 示例用法
color_transformed_image = random_color_transform(image)
# 显示结果
cv2.imshow('Color Transformed Image', color_transformed_image)
# 显示结果
cv2.imshow('Original Image', image)
cv2.imshow('Brightened Image', bright_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""