import base64
import zlib

# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     return encoded_string
#
# def compress_base64(base64_string):
#     compressed_data = zlib.compress(base64_string.encode('utf-8'),level=9)
#     return base64.b64encode(compressed_data).decode('utf-8')
#
#
# # 使用示例
image_path = "D:/Bingo/data/testImages/1.jpg"  # 替换为你的图片路径
# base64_string = image_to_base64(image_path)
# compressed_base64_string = compress_base64(base64_string)
# print(base64_string)
# print(compressed_base64_string)
# print(len(base64_string),len(compressed_base64_string))

with open(image_path, "rb") as image_file:
         data = base64.b64encode(image_file.read()).decode('utf-8')

print(len(data))
print(data)

# 压缩
compressed_data = zlib.compress(data.encode(),level=9)  # 注意：这儿要以字节的形式传入
print(len(compressed_data))
