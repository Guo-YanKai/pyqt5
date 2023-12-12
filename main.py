import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
# from PyQt5.QtGui import  QPixmap
from ImageSelector import ImageSelector

STATUS_MAPPING = {
    "0": "初始化中",
    "1": "待执行",
    "2": "正在执行",
    "3": "完成并提醒",
    "10": "异常并停止",
    "12": "初始化失败",
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 控件
        self.txt_asin = None
        self.table_widget = None

        # 窗体标题和尺寸
        self.setWindowTitle("xx系统")

        # 窗体的尺寸
        self.resize(1228, 500),

        # 窗口的位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 垂直方向的布局
        layout = QVBoxLayout()
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_form())
        layout.addLayout(self.init_table())
        layout.addLayout(self.init_footer())

        # 给窗体设置元素的排列方式
        self.setLayout(layout)

    def init_header(self):
        # 1、创建顶部菜单布局
        header_layout = QHBoxLayout()

        # 1.1 创建按钮
        btn_start = QPushButton("开始")
        # btn_start.setFixedSize(30, 30)
        header_layout.addWidget(btn_start)

        btn_stop = QPushButton("暂停")
        header_layout.addWidget(btn_stop)
        header_layout.addStretch()

        # 创建一个按钮控件用于打开文件对话框
        select_button = QPushButton('Select Image', self)
        select_button.setGeometry(150, 360, 100, 30)
        # 链接按钮触发函数
        # select_button.clicked.connect(self.select_image)
        header_layout.addWidget(select_button)

        return header_layout

    def select_image(self):
        """打开一个图片"""
        image_selector = ImageSelector()
        image_selector.show()

    def init_form(self):
        # 2、创建顶部菜单布局
        form_layout = QHBoxLayout()

        # 2.1添加输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID:")
        txt_asin.setText("a=100")
        self.txt_asin = txt_asin
        form_layout.addWidget(txt_asin)

        # 2.2添加按钮
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)

        form_layout.addWidget(btn_add)
        return form_layout

    def init_table(self):
        # 3、创建中间表格布局
        table_layout = QHBoxLayout()

        # 3.1创建表格对象
        table_widget = QTableWidget(0, 8)
        table_widget.horizontalHeader().setStyleSheet(
            "color: rgb(0, 0, 0);border:1px solid rgb(210, 210, 210);")  # 设置表头颜色

        tabel_header = [
            {"field": "asin", "text": "ASIN", "width": 120},
            {"field": "title", "text": "标题", "width": 150},
            {"field": "url", "text": "URL", 'width': 400},
            {"field": "price", "text": "底价", "width": 100},
            {"field": "success", "text": "成功次数", 'width': 100},
            {"field": "error", "text": "503次数", 'width': 100},
            {"field": "status", "text": "状态", 'width': 100},
            {"field": "frequency", "text": "频率(N秒/次)", 'width': 100}

        ]
        for idx, info in enumerate(tabel_header):
            item = QTableWidgetItem()
            item.setText(info["text"])
            table_widget.setHorizontalHeaderItem(idx, item)
            table_widget.setColumnWidth(idx, info["width"])

        # 3.2表格数据初始化
        import json
        with open("./db/db.json") as file:
            data_list = json.load(file)

        # 获取表格的当前行
        current_row_count = table_widget.rowCount()
        for row_list in data_list:
            table_widget.insertRow(current_row_count)
            # 写数据
            for i, colum in enumerate(row_list):
                item = QTableWidgetItem()
                if i == 6:
                    item.setText(STATUS_MAPPING[str(colum)])
                else:
                    item.setText(str(colum))
                if i in [0, 4, 5, 6]:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table_widget.setItem(current_row_count, i, item)

            current_row_count += 1

        self.table_widget = table_widget
        table_layout.addWidget(table_widget)
        return table_layout

    def init_footer(self):
        # 4、创建底部菜单
        footer_layout = QHBoxLayout()

        label_status = QLabel()
        label_status.setText("未检测")
        footer_layout.addWidget(label_status)

        footer_layout.addStretch()

        btn_reinit = QPushButton("重新初始化")
        btn_reinit.clicked.connect(self.event_reinit_click)
        footer_layout.addWidget(btn_reinit)

        btn_redetect = QPushButton("重新检测")
        footer_layout.addWidget(btn_redetect)

        btn_zero = QPushButton("次数清零")
        btn_zero.clicked.connect(self.event_zero_click)
        footer_layout.addWidget(btn_zero)

        btn_delet = QPushButton("删除检测项")
        footer_layout.addWidget(btn_delet)

        btn_cfg = QPushButton("SMTP报警配置")
        footer_layout.addWidget(btn_cfg)

        btn_proxy = QPushButton("代理IP")
        footer_layout.addWidget(btn_proxy)
        return footer_layout

    def event_add_click(self):
        # 1、读取输入框中的内容
        text = self.txt_asin.text().strip()

        if not text:
            QMessageBox.warning(self, 'Warning', '商品的ASIN输入为空!')
            return
        asin, price = text.split("=")
        price = float(price)

        # 2、将内容加入到表格中(基本数据)
        new_row = [asin, "", "", price, 0, 0, 0, 5]

        # 获取表格的当前行
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)  # 添加行
        for i, colum in enumerate(new_row):
            item = QTableWidgetItem()
            if i == 6:
                item.setText(STATUS_MAPPING[str(colum)])
            else:
                item.setText(str(colum))
            if i in [0, 4, 5, 6]:
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(current_row_count, i, item)

        # 3、爬虫请求自动获取标题
        # 不能在主线程中做爬虫的事，需要创建一个线程去做爬虫，爬取的数据更新到窗体应用(信号)
        from utils.threads import NewTaskThread
        thread = NewTaskThread(current_row_count, asin, self)
        thread.success.connect(self.init_task_success_callback)
        thread.error.connect(self.init_task_error_callback)
        thread.start()

    def init_task_success_callback(self, index, asin, title, url):
        """更新窗体显示的数据"""
        # 更新标题列
        cell_title = QTableWidgetItem(title)
        cell_title.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 1, cell_title)
        # 更新url
        cell_url = QTableWidgetItem(url)
        cell_url.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 2, cell_url)

        cell_status = QTableWidgetItem(STATUS_MAPPING["1"])
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 6, cell_status)

        # 清空输入框
        self.txt_asin.clear()

        pass

    def init_task_error_callback(self, index, asin, title, url):

        # 更新标题列
        cell_title = QTableWidgetItem(title)
        cell_title.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 1, cell_title)
        # 更新url
        cell_url = QTableWidgetItem(url)
        cell_url.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 2, cell_url)
        # 更新状态
        cell_status = QTableWidgetItem(STATUS_MAPPING["11"])
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(index, 6, cell_status)

        self.txt_asin.clear()

    def event_reinit_click(self):
        # 获取选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "没有选中数据!")
            return

        for row_object in row_list:
            index = row_object.row()

            asin = self.table_widget.item(index, 0).text().strip()  # 获取某一列

            # 更新状态
            cell_status = QTableWidgetItem(STATUS_MAPPING["0"])
            cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(index, 6, cell_status)

            # 创建线程进行初始化的动作

            from utils.threads import NewTaskThread

            thread = NewTaskThread(index, asin, self)
            thread.success.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()

    def event_zero_click(self):
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "没有选中数据!")
            return
        for row_object in row_list:
            index = row_object.row()
            cell_succ = QTableWidgetItem(str(0))
            cell_succ.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(index, 4, cell_succ)

            cell_num = QTableWidgetItem(str(0))
            cell_num.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(index, 5, cell_num)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
