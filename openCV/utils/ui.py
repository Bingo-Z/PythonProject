import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QFileDialog, QListWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from utils.dataLoad import read_images_from_folder, read_matching_text, save_image_and_boxes, \
    display_image_with_boxes


class DataAugmentationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.images = []  # 存储图片数据的列表
        self.current_image = None  # 当前显示的图片
        self.current_boxes = None  # 当前图片的边界框数据
        self.labels_path = None  # 存储labels文件夹路径

    def initUI(self):
        # 设置主窗口属性
        self.setWindowTitle('数据增强工具')
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # 创建左侧布局
        left_layout = QVBoxLayout()

        # 添加图片文件夹选择标签
        self.folder_label = QLabel('请选择图片文件夹', self)
        left_layout.addWidget(self.folder_label)

        # 添加选择图片文件夹按钮
        self.select_button = QPushButton('选择图片文件夹', self)
        self.select_button.clicked.connect(self.selectImageFolder)
        left_layout.addWidget(self.select_button)

        # 添加labels文件夹选择标签
        self.labels_label = QLabel('请选择labels文件夹', self)
        left_layout.addWidget(self.labels_label)

        # 添加选择labels文件夹按钮
        self.select_labels_button = QPushButton('选择labels文件夹', self)
        self.select_labels_button.clicked.connect(self.selectLabelsFolder)
        left_layout.addWidget(self.select_labels_button)

        # 添加图片列表
        self.image_list = QListWidget(self)
        self.image_list.itemClicked.connect(self.displayImage)
        left_layout.addWidget(self.image_list)

        # 添加数据增强按钮
        self.augment_button = QPushButton('数据增强', self)
        self.augment_button.clicked.connect(self.augmentData)
        left_layout.addWidget(self.augment_button)

        # 创建右侧布局
        right_layout = QVBoxLayout()

        # 添加图片显示区域
        self.image_view = QGraphicsView(self)
        self.image_scene = QGraphicsScene(self)
        self.image_view.setScene(self.image_scene)
        right_layout.addWidget(self.image_view)

        # 将左右布局添加到主布局
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # 设置中央部件的布局
        central_widget.setLayout(main_layout)

    def selectImageFolder(self):
        # 打开图片文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, '选择图片文件夹')
        if folder_path:
            # 更新标签显示选中的文件夹路径
            self.folder_label.setText(f'已选择图片文件夹: {folder_path}')
            # 读取文件夹中的图片
            self.images = read_images_from_folder(folder_path)
            # 更新图片列表
            self.updateImageList()

    def selectLabelsFolder(self):
        # 打开labels文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, '选择labels文件夹')
        if folder_path:
            # 更新标签显示选中的文件夹路径
            self.labels_label.setText(f'已选择labels文件夹: {folder_path}')
            # 存储labels文件夹路径
            self.labels_path = folder_path

    def updateImageList(self):
        # 清空当前列表
        self.image_list.clear()
        # 将读取到的图片文件名添加到列表中
        for file_name, _ in self.images:
            self.image_list.addItem(file_name)

    def displayImage(self, item):
        # 获取选中的文件名
        file_name = item.text()
        for name, img in self.images:
            if name == file_name:
                # 更新当前图片
                self.current_image = img
                # 读取对应的txt文件
                if self.labels_path:
                    txt_file_path = os.path.join(self.labels_path, os.path.splitext(name)[0] + '.txt')
                    self.current_boxes = read_matching_text(name, txt_file_path)
                else:
                    self.current_boxes = []

                # 在图片上绘制边界框
                img_with_boxes = display_image_with_boxes(img, self.current_boxes)

                # 将OpenCV图像转换为QImage
                height, width, channel = img_with_boxes.shape
                bytes_per_line = 3 * width
                q_img = QImage(img_with_boxes.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(q_img)

                # 在图形场景中显示图片
                self.image_scene.clear()
                self.image_scene.addPixmap(pixmap)
                self.image_view.fitInView(self.image_scene.sceneRect(), Qt.KeepAspectRatio)
                break

    def augmentData(self):
        # 检查是否有当前图片和边界框数据
        if self.current_image is not None and self.current_boxes is not None:
            # 选择保存文件夹
            save_path = QFileDialog.getExistingDirectory(self, '选择保存文件夹')
            if save_path:
                # 保存增强后的图片和边界框信息
                # 注意：这里可以添加更多的数据增强方法
                save_image_and_boxes(self.current_image, self.current_boxes, save_path, 'aug_',
                                     self.image_list.currentItem().text())

    def resizeEvent(self, event):
        # 处理窗口大小变化事件
        super().resizeEvent(event)
        # 调整图片显示以适应新的窗口大小
        if self.image_scene.items():
            self.image_view.fitInView(self.image_scene.sceneRect(), Qt.KeepAspectRatio)


def main():
    # 创建QApplication实例
    app = QApplication(sys.argv)
    # 创建并显示主窗口
    ui = DataAugmentationUI()
    ui.show()
    # 运行应用程序的主循环
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()