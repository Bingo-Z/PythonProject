import cv2
import numpy as np


def extract_table(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像文件")
        return

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用高斯模糊以减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 查找轮廓，使用RETR_TREE以保留所有轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个白色背景图像
    table_image = np.ones_like(image) * 255  # 白色背景

    # 绘制轮廓
    for contour in contours:
        # 只绘制较大的轮廓
        if cv2.contourArea(contour) > 3050:  # 可以根据需要调整阈值
            cv2.drawContours(table_image, [contour], -1, (0, 0, 0), 2)  # 黑色轮廓

    # 将原始图像的文字区域设置为白色
    mask = np.zeros_like(gray)
    for contour in contours:
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    # 使用掩膜去除文字
    result = cv2.bitwise_and(table_image, table_image, mask=mask)

    # 显示结果
    cv2.imshow("Extracted Table", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = r"D:\Bingo\openCV\data\3\augmented_1.jpg"  # 替换为你的表格图像路径
    extract_table(image_path) 