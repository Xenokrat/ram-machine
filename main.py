import json
import sys
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QMessageBox,
    QWidget,
)

from ram_machine.command import Commands
from ram_machine.program import Program
from ram_machine.register import Register
from ram_machine.tapes import InputTape, OutputTape
from ram_machine.ui import Ui_Form


class RamMachine(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.program = Program(
            command_cls=Commands,
            reg=Register({}),
            input_tape=InputTape([]),
            output_tape=OutputTape(),
            command_str_list=[],
            current_command=0,
        )
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.update_ui()

        self.worker = Worker(self.program)
        self.worker.step_signal.connect(self.step)

        # Input Commands
        self.ui.line_edit_command.returnPressed.connect(self.add_or_edit_command)
        self.ui.col_commands.itemDoubleClicked.connect(self.edit_selected_command)
        self.ui.col_commands.itemChanged.connect(self.set_or_update_program)
        self.ui.col_commands.itemChanged.connect(self.update_ui)
        self.ui.col_commands.itemEntered.connect(self.set_or_update_program)
        self.ui.col_commands.itemEntered.connect(self.update_ui)
        self.ui.btn_del_command.clicked.connect(self.delete_command)
        self.ui.btn_del_command.clicked.connect(self.set_or_update_program)
        self.ui.btn_del_command.clicked.connect(self.update_ui)

        # Input Values
        self.ui.line_edit_value.returnPressed.connect(self.add_or_edit_value)
        self.ui.col_itape.itemDoubleClicked.connect(self.edit_selected_value)
        self.ui.col_itape.itemChanged.connect(self.set_or_update_program)
        self.ui.col_itape.itemEntered.connect(self.set_or_update_program)
        self.ui.btn_del_input.clicked.connect(self.delete_input)
        self.ui.btn_del_input.clicked.connect(self.set_or_update_program)
        self.ui.btn_del_input.clicked.connect(self.update_ui)

        # New
        self.ui.btn_new.clicked.connect(self.new)

        # Step
        self.ui.btn_step.clicked.connect(self.step)

        # Run | Stop
        self.ui.btn_run.clicked.connect(self.run)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.worker.stop_btn_signal.connect(self.__unblock_buttons)

        # Save | Load
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_load.clicked.connect(self.load)

    def refresh_output(self) -> None:
        if self.program is None:
            return
        items = [str(i) for i in self.program.output_tape.data]
        self.ui.col_otape.clear()
        self.ui.col_otape.addItems(items)

    def new(self) -> None:
        self.ui.col_commands.clear()
        self.ui.col_itape.clear()
        self.program.current_command = 0
        self.program.input_tape.current_cell = 0
        self.set_or_update_program()
        self.program.output_tape.clear()
        self.update_ui()

    def save(self) -> None:
        commands = self.get_commands()
        input = self.get_itape_values()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save State",
            "program", "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return
        with open(file_path, "w") as f:
            data = json.dumps({"commands": commands, "input": input,})
            f.writelines(data)

    def load(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Save State",
            "./saved_states", "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return
        with open(file_path, "r") as f:
            data = json.load(f)
        self.ui.col_commands.clear()
        self.ui.col_commands.addItems(data["commands"])
        self.ui.col_itape.clear()
        self.ui.col_itape.addItems([str(i) for i in data["input"]])
        self.set_or_update_program()

    def update_ui(self) -> None:
        try:
            ind = self.program.current_command
            text = self.program.command_str_list[ind]
        except IndexError:
            text = "None"
        except AttributeError:
            text = "None"
        self.ui.text_cur_command.setText(text)

    def add_or_edit_command(self) -> None:
        text = self.ui.line_edit_command.text().strip()
        if text:
            selected_item = self.ui.col_commands.currentItem()
            if selected_item:
                selected_item.setText(text)
            else:
                item = QListWidgetItem(text)
                self.ui.col_commands.addItem(item)
            self.ui.line_edit_command.clear()
            self.ui.col_commands.clearSelection()

    def edit_selected_command(self, item) -> None:
        self.ui.line_edit_command.setText(item.text())
        self.ui.line_edit_command.selectAll()
        self.ui.line_edit_command.setFocus()

    def add_or_edit_value(self) -> None:
        text = self.ui.line_edit_value.text().strip()
        if text:
            selected_item = self.ui.col_itape.currentItem()
            if selected_item:
                selected_item.setText(text)
            else:
                item = QListWidgetItem(text)
                self.ui.col_itape.addItem(item)
            self.ui.line_edit_value.clear()
            self.ui.col_itape.clearSelection()

    def edit_selected_value(self, item) -> None:
        self.ui.line_edit_value.setText(item.text())
        self.ui.line_edit_value.selectAll()
        self.ui.line_edit_value.setFocus()

    def get_commands(self) -> list[str]:
        commands = []
        for index in range(self.ui.col_commands.count()):
            item = self.ui.col_commands.item(index)
            commands.append(item.text())
        return commands

    def get_itape_values(self) -> list[int]:
        values = []
        try:
            for index in range(self.ui.col_itape.count()):
                item = self.ui.col_itape.item(index)
                values.append(int(item.text()))
        except ValueError as e:
            QMessageBox.critical(self, type(e).__name__, str(e))
            return []
        return values

    def step(self) -> None:
        try:
            self.program.exec_command()
        except Exception as e:
            self.program.running = False
            QMessageBox.critical(self, type(e).__name__, str(e))
        self.refresh_output()
        self.update_ui()

    def run(self) -> None:
        self.worker.delay = self.ui.box_delay.value()
        self.__block_buttons_during_loop()
        if not self.worker.isRunning():
            self.worker.start()

    def stop(self) -> None:
        if self.worker.isRunning():
            self.worker.stop()

    def __block_buttons_during_loop(self) -> None:
        self.ui.btn_load.setEnabled(False)
        self.ui.btn_new.setEnabled(False)
        self.ui.btn_run.setEnabled(False)
        self.ui.btn_save.setEnabled(False)
        self.ui.btn_step.setEnabled(False)
        self.ui.btn_del_command.setEnabled(False)
        self.ui.btn_del_input.setEnabled(False)
        self.ui.line_edit_command.setEnabled(False)
        self.ui.line_edit_value.setEnabled(False)

    def __unblock_buttons(self) -> None:
        self.ui.btn_load.setEnabled(True)
        self.ui.btn_new.setEnabled(True)
        self.ui.btn_run.setEnabled(True)
        self.ui.btn_save.setEnabled(True)
        self.ui.btn_step.setEnabled(True)
        self.ui.btn_del_command.setEnabled(True)
        self.ui.btn_del_input.setEnabled(True)
        self.ui.line_edit_command.setEnabled(True)
        self.ui.line_edit_value.setEnabled(True)

    def set_or_update_program(self) -> None:
        input_values = self.get_itape_values()
        commands = self.get_commands()
        self.program.input_tape = InputTape(input_values)
        self.program.command_str_list = commands

    def delete_command(self) -> None:
        selected = self.ui.col_commands.selectedItems()
        for item in selected:
            self.ui.col_commands.takeItem(self.ui.col_commands.row(item))

    def delete_input(self) -> None:
        selected = self.ui.col_itape.selectedItems()
        for item in selected:
            self.ui.col_itape.takeItem(self.ui.col_itape.row(item))


class Worker(QThread):
    step_signal = pyqtSignal()
    stop_btn_signal = pyqtSignal()

    def __init__(self, program: Program) -> None:
        super().__init__()
        self.program = program
        self.program.running = False
        self.delay = 0.5

    def run(self) -> None:
        self.program.running = True
        while self.program.running:
            self.step_signal.emit()
            sleep(self.delay)
        self.stop()

    def stop(self) -> None:
        self.program.running = False
        self.stop_btn_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RamMachine()
    window.show()
    sys.exit(app.exec())
