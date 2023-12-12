import time

from PyQt5.QtCore import QThread, pyqtSignal


class NewTaskThread(QThread):

    # 信号，触发信号，更新窗体中的数据
    success = pyqtSignal(int, str, str, str)
    error = pyqtSignal(int, str, str, str)

    def __init__(self, row_index,asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_index = row_index
        self.asin = asin

    def run(self):
        """具体线程做的事"""
        try:
            # 具体要做的事
            time.sleep(5)
            self.success.emit(self.row_index, self.asin, "cpu", "www.baidu.com")

        except Exception as e:
           self.error.emit(self.row_index, self.asin, "error", str(e))
