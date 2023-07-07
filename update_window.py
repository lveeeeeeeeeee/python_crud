# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sql_foundation as sq


class Ui_UPDATE(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("UPDATE")
        MainWindow.resize(340, 300)
        MainWindow.setMinimumSize(QtCore.QSize(340, 300))
        MainWindow.setMaximumSize(QtCore.QSize(440, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setObjectName("table_view")
        self.gridLayout.addWidget(self.table_widget, 1, 0, 1, 2)
        self.button_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.button_cancel.setObjectName("button_cancel")
        self.gridLayout.addWidget(self.button_cancel, 2, 0, 1, 1)
        self.button_confirm = QtWidgets.QPushButton(self.centralwidget)
        self.button_confirm.setObjectName("button_confirm")
        self.gridLayout.addWidget(self.button_confirm, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.item_conditions = None
        self.MainWindow = MainWindow

        self.connect(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("UPDATE", "UPDATE"))
        self.label.setText(_translate("UPDATE", "Input the new values for selected items"))
        self.button_cancel.setText(_translate("UPDATE", "Cancel"))
        self.button_confirm.setText(_translate("UPDATE", "Confirm"))
    
    def connect(self, MainWindow):
        self.button_cancel.clicked.connect(MainWindow.close)
        self.button_confirm.clicked.connect(self.update_items)

    def handle(self, e: Exception):
        msg = QtWidgets.QMessageBox.about(
            self.MainWindow,
            "ERROR", 
            f"Error!\n{e.args[0]}\nThe query wasn't completed"
        )
        self.MainWindow.close()

    def get_item_conditions(self, item_conds):
        self.item_conditions = item_conds
    
    def fill_the_table(self, tablename):
        self.tablename = tablename
        columns = sq.select(
            None, tablename="information_schema.columns",
            to_select="column_name",
            cond=f"table_name = '{tablename}'",
            limit=0
        )
        self.table_widget.clear()
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(["Column names", "Input"])
        for i in range(len(columns)):
            item = QtWidgets.QTableWidgetItem(f"{columns[i][0]}")
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem("")
            self.table_widget.setItem(i, 1, item)
        self.table_widget.resizeColumnsToContents()

    def update_items(self):
        connection = None
        cursor = None
        i = 0
        try:
            for elem in self.item_conditions:
                i += 1
                row_count = self.table_widget.rowCount()
                columns = []
                values = []
                for i in range(row_count):
                    value = self.table_widget.item(i, 1).text()
                    if value.isdigit():
                        values.append(value)
                    elif value != "":
                        values.append(f"'{value}'")
                    else:
                        continue
                    columns.append(self.table_widget.item(i, 0).text())

                connection = sq.ret_connection(self.handle)
                values = sq._pack_update_vals(columns=columns, vals=values)
                cursor = connection.cursor()
                cursor.execute(f"UPDATE {self.tablename} SET {values} WHERE ({elem})")
                connection.commit()
                
            self.MainWindow.close()

        except Exception as e:
            self.handle(e)

        finally:
            if connection != None:
                connection.close()
            if cursor != None:
                cursor.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_UPDATE()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
