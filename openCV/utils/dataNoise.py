#高斯噪声
import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, sigma=25):
    # 生成与图像相同大小的高斯噪声
    gaussian_noise = np.random.normal(mean, sigma, image.shape).astype(np.uint8)
    # 将噪声添加到图像中
    noisy_image = cv2.add(image, gaussian_noise)
    return noisy_image

# 读取图像
image = cv2.imread('path/to/your/image.jpg')
# 添加噪声
noisy_image = add_gaussian_noise(image)
# 显示结果
cv2.imshow('Noisy Image', noisy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#椒盐噪声

def add_salt_and_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
    noisy_image = np.copy(image)
    total_pixels = image.size
    # 添加盐噪声
    num_salt = np.ceil(salt_prob * total_pixels)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[coords[0], coords[1], :] = 1  # 盐噪声为白色

    # 添加胡椒噪声
    num_pepper = np.ceil(pepper_prob * total_pixels)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[coords[0], coords[1], :] = 0  # 胡椒噪声为黑色

    return noisy_image

# 添加椒盐噪声
salt_and_pepper_image = add_salt_and_pepper_noise(image)
# 显示结果
cv2.imshow('Salt and Pepper Image', salt_and_pepper_image)
cv2.waitKey(0)
cv2.destroyAllWindows()