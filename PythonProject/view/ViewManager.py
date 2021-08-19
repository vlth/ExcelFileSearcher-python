import sys
from PyQt5.QtWidgets import QApplication, QLabel


class ViewManager:
    def show_application(self):
        app = QApplication([])
        label = QLabel('JuraFun')
        label.show()
        app.exec()
