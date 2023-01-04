import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, \
    QGridLayout, QMessageBox

from logic import generate_problem, Problem, Results

russian = {
    'ANSWER': "Ответ",
    'INPUT_WARNING': "Можно отвечать только цифрами!",
    'CORRECT_ANSWERS': "Правильные ответы",
    'INCORRECT_ANSWERS': "Неправильные ответы",
}

english = {
    'ANSWER': "Answer",
    'INPUT_WARNING': "Only numbers!",
    'CORRECT_ANSWERS': "Correct answers",
    'INCORRECT_ANSWERS': "Incorrect answers",
}

language = english if '-english' in sys.argv else russian


def load_font(font):
    try:
        return QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(font))[0]
    except IndexError:
        dialog = QMessageBox()
        dialog.setWindowTitle("Error")
        dialog.setText(f"Font '{font}' not found, continue with default font?")
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        button = dialog.exec()
        if button == QMessageBox.StandardButton.No:
            raise
        return 'default'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        font = QFont(load_font('Inter.ttf'), 30)
        font.setStyleStrategy(font.StyleStrategy.PreferAntialias)

        self.setWindowTitle("Генератор выражений 1.0")

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.label.setFont(font)

        font.setPixelSize(20)

        self.input = QLineEdit()
        self.input.setFixedSize(QSize(400, 50))
        self.input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.input.setFont(font)

        self.submit = QPushButton()
        self.submit.setFixedSize(QSize(400, 50))
        self.submit.setText(language['ANSWER'])
        self.submit.clicked.connect(self.check_answer)

        self.warning_label = QLabel()
        self.setFont(font)
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.results_label = QLabel()
        self.setFont(font)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QGridLayout()
        # layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.input, 2, 0)
        layout.addWidget(self.submit, 3, 0)
        layout.addWidget(self.warning_label, 4, 0)
        layout.addWidget(self.results_label, 5, 0)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setMinimumSize(QSize(400, 500))

        self.current_problem: Problem | None = None

        self.setContentsMargins(20, 60, 20, 20)

        self.results = Results()

        self.setStyleSheet('background-color: #1A1A1A; color: white')
        self.input.setStyleSheet('border: 1px solid white')
        self.submit.setStyleSheet('border: unset; background-color: #313131')

    def show_problem(self):
        self.current_problem = generate_problem(20, 40)

        self.label.setText(str(self.current_problem))

    def check_answer(self):
        answer = self.input.text()
        if not answer:
            return

        self.input.setText(None)
        if not answer.isnumeric():
            self.warning_label.setText(language['INPUT_WARNING'])
            return
        self.warning_label.setText(None)
        if int(answer) == self.current_problem.answer:
            self.results.correct += 1
        else:
            self.results.incorrect += 1
        self.update_results()
        self.show_problem()

    def update_results(self):
        text = (f"{language['CORRECT_ANSWERS']}: {self.results.correct}"
                f"\n{language['INCORRECT_ANSWERS']}: {self.results.incorrect}")
        self.results_label.setText(text)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and self.input.hasFocus():
            self.check_answer()
        super().keyPressEvent(event)

    def show(self):
        super().show()
        self.show_problem()


class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.window = MainWindow()
        self.window.show()


if __name__ == '__main__':
    app = App()
    app.exec()
