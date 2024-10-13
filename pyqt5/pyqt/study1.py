import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()

    #设置窗口标题
    w.setWindowTitle("First pyqt5")

    #添加控件
    btn = QPushButton("这是一个按钮")
    #将按钮添加到父窗口
    btn.setParent(w)
    #文本
    label = QLabel("图片路径：",w)
    #显示位置和大小
    label.setGeometry(100,100,400,400)
    #文本框
    edit = QLineEdit(w)
    edit.setPlaceholderText("请输入图片存储路径....")
    edit.setGeometry(160,290,200,20)


    w.move(400,400)

    #窗口展示
    w.show()

    #程序进入循环状态
    app.exec_()