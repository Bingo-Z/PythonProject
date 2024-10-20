import cv2


def flip_image(image, flip_code):
    """
    使用OpenCV对图片进行翻转
    :param image: 输入的图像数据（numpy数组）
    :param flip_code: 翻转方式
        0 - 沿X轴翻转（上下翻转）
        1 - 沿Y轴翻转（左右翻转）
        -1 - 同时沿X轴和Y轴翻转（上下左右翻转）
    :return: 翻转后的图像
    """
    return cv2.flip(image, flip_code)