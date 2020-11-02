# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:46:23 2020

@author: lindineu.duran
"""

import sys
from PyQt5.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QApplication


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        layout = QVBoxLayout()

        cb_dict = {"cb1": False, "cb2": True, "cb3": False}
        cb_widget_list = list()

        for checkbox in cb_dict:
            widget = QCheckBox(checkbox)
            widget.stateChanged.connect(
                lambda state, checkbox=checkbox: self.update(state, checkbox)  # +++
            )
            cb_widget_list.append(widget)

        for widget in cb_widget_list:
            layout.addWidget(widget)
        self.setLayout(layout)

    def update(self, state, origin: str):                                      # + state
        print("Checkbox {} has changed: {}".format(origin, state))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())