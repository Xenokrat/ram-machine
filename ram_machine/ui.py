# Form implementation generated from reading ui file 'ui/ram_machine.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_new = QtWidgets.QPushButton(parent=Form)
        self.btn_new.setObjectName("btn_new")
        self.verticalLayout_4.addWidget(self.btn_new)
        self.line = QtWidgets.QFrame(parent=Form)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.btn_step = QtWidgets.QPushButton(parent=Form)
        self.btn_step.setObjectName("btn_step")
        self.verticalLayout_4.addWidget(self.btn_step)
        self.btn_run = QtWidgets.QPushButton(parent=Form)
        self.btn_run.setObjectName("btn_run")
        self.verticalLayout_4.addWidget(self.btn_run)
        self.label_7 = QtWidgets.QLabel(parent=Form)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.box_delay = QtWidgets.QDoubleSpinBox(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_delay.setFont(font)
        self.box_delay.setDecimals(1)
        self.box_delay.setMinimum(0.1)
        self.box_delay.setMaximum(5.0)
        self.box_delay.setSingleStep(0.1)
        self.box_delay.setProperty("value", 0.5)
        self.box_delay.setObjectName("box_delay")
        self.verticalLayout_4.addWidget(self.box_delay)
        self.btn_stop = QtWidgets.QPushButton(parent=Form)
        self.btn_stop.setObjectName("btn_stop")
        self.verticalLayout_4.addWidget(self.btn_stop)
        self.line_2 = QtWidgets.QFrame(parent=Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.btn_load = QtWidgets.QPushButton(parent=Form)
        self.btn_load.setObjectName("btn_load")
        self.verticalLayout_4.addWidget(self.btn_load)
        self.btn_save = QtWidgets.QPushButton(parent=Form)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout_4.addWidget(self.btn_save)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line_edit_command = QtWidgets.QLineEdit(parent=Form)
        self.line_edit_command.setText("")
        self.line_edit_command.setObjectName("line_edit_command")
        self.verticalLayout.addWidget(self.line_edit_command)
        self.btn_del_command = QtWidgets.QPushButton(parent=Form)
        self.btn_del_command.setObjectName("btn_del_command")
        self.verticalLayout.addWidget(self.btn_del_command)
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.col_commands = QtWidgets.QListWidget(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.col_commands.setFont(font)
        self.col_commands.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.col_commands.setObjectName("col_commands")
        self.verticalLayout.addWidget(self.col_commands)
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.text_cur_command = QtWidgets.QTextBrowser(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_cur_command.setFont(font)
        self.text_cur_command.setObjectName("text_cur_command")
        self.verticalLayout.addWidget(self.text_cur_command)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=Form)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.line_edit_value = QtWidgets.QLineEdit(parent=Form)
        self.line_edit_value.setObjectName("line_edit_value")
        self.verticalLayout_2.addWidget(self.line_edit_value)
        self.btn_del_input = QtWidgets.QPushButton(parent=Form)
        self.btn_del_input.setObjectName("btn_del_input")
        self.verticalLayout_2.addWidget(self.btn_del_input)
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.col_itape = QtWidgets.QListWidget(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.col_itape.setFont(font)
        self.col_itape.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.col_itape.setObjectName("col_itape")
        self.verticalLayout_2.addWidget(self.col_itape)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.col_otape = QtWidgets.QListWidget(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.col_otape.setFont(font)
        self.col_otape.setObjectName("col_otape")
        self.verticalLayout_3.addWidget(self.col_otape)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_new.setText(_translate("Form", "New"))
        self.btn_step.setText(_translate("Form", "Step"))
        self.btn_run.setText(_translate("Form", "Run"))
        self.label_7.setText(_translate("Form", "Delay"))
        self.btn_stop.setText(_translate("Form", "Stop"))
        self.btn_load.setText(_translate("Form", "Load"))
        self.btn_save.setText(_translate("Form", "Save"))
        self.label.setText(_translate("Form", "Add command"))
        self.line_edit_command.setPlaceholderText(_translate("Form", "Type new command and press Enter"))
        self.btn_del_command.setText(_translate("Form", "Delete command(s)"))
        self.label_5.setText(_translate("Form", "Commands"))
        self.label_4.setText(_translate("Form", "Current Command"))
        self.label_6.setText(_translate("Form", "Add Value"))
        self.line_edit_value.setPlaceholderText(_translate("Form", "Type new value and press Enter"))
        self.btn_del_input.setText(_translate("Form", "Delete input(s)"))
        self.label_2.setText(_translate("Form", "Input Tape"))
        self.label_3.setText(_translate("Form", "Output Tape"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
