from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap


class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Selector')
        self.setGeometry(100, 100, 400, 400)

        # 创建一个标签控件用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 300, 300)

        # 创建一个按钮控件用于打开文件对话框
        self.select_button = QPushButton('Select Image', self)
        self.select_button.setGeometry(150, 360, 100, 30)
        # 链接按钮触发函数
        self.select_button.clicked.connect(self.select_image)

    def select_image(self):
        # 打开文件对话框以选择一个图片文件
        file_dialog = QFileDialog(self)
        # 图片格式为bmp、png和jpg
        file_dialog.setNameFilter("Image files (*.bmp *.png *.jpg)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            # 加载选择的图片文件
            image_file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(image_file_path)
            self.image_label.setPixmap(pixmap)


