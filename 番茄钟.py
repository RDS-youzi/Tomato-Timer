import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon

class ArknightsPotatoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tomato Timer')
        self.setGeometry(100, 100, 400, 200)

        self.time_left = 25 * 60
        self.break_time = 10 * 60
        self.paused = False
        self.on_break = False

        self.layout = QVBoxLayout()

        self.label_timer = QLabel(self.format_time(self.time_left), self)
        font = self.label_timer.font()
        font.setFamily("幼圆")
        font.setPointSize(40)
        self.label_timer.setFont(font)
        self.label_timer.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_timer)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(self.time_left)
        self.progress_bar.setValue(self.time_left)
        self.layout.addWidget(self.progress_bar)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setStyleSheet("QPushButton { background-color: #2E2925; color: #E5E1DD; font-size: 18px; border-radius: 10px;}"
                                       "QPushButton:hover { background-color: #413C38; }")
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setStyleSheet("QPushButton { background-color: #2E2925; color: #E5E1DD; font-size: 18px; border-radius: 10px;}"
                                       "QPushButton:hover { background-color: #413C38; }")
        self.pause_button.setEnabled(False)
        self.layout.addWidget(self.pause_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setStyleSheet("QPushButton { background-color: #E5E1DD; color: #2E2925; font-size: 18px; border-radius: 10px;}"
                                        "QPushButton:hover { background-color: #D3CDC6; }")
        self.layout.addWidget(self.reset_button)

        self.label_count = QLabel('Tomato Count: 0', self)
        self.label_count.setStyleSheet("QLabel { color: #333333; font-size: 14px; }")
        self.layout.addWidget(self.label_count)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.create_tray_icon()

    def start_timer(self):
        if not self.on_break:
            self.paused = False
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.timer.start(1000)
        else:
            self.start_break_timer()

    def start_break_timer(self):
        self.paused = False
        self.on_break = True
        self.time_left = self.break_time
        self.label_timer.setText(self.format_time(self.time_left))
        self.progress_bar.setMaximum(self.time_left)
        self.progress_bar.setValue(self.time_left)
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.timer.start(1000)

    def pause_timer(self):
        self.paused = True
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def reset_timer(self):
        self.timer.stop()
        if not self.on_break:
            self.time_left = 25 * 60
        else:
            self.time_left = self.break_time
            self.on_break = False
        self.label_timer.setText(self.format_time(self.time_left))
        self.progress_bar.setMaximum(self.time_left)
        self.progress_bar.setValue(self.time_left)
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.paused = False

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label_timer.setText(self.format_time(self.time_left))
            self.progress_bar.setValue(self.time_left)
        else:
            self.timer.stop()
            if not self.on_break:
                self.label_timer.setText("Time's up! Take a break!")
                self.start_button.setEnabled(True)
                self.pause_button.setEnabled(False)
                self.paused = False
                self.tomato_count += 1
                self.label_count.setText(f'Tomato Count: {self.tomato_count}')
            else:
                self.label_timer.setText("Break's over! Start working!")
                self.start_timer()

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f'{minutes:02d}:{seconds:02d}'

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = 'icon(path)'
        self.tray_icon.setIcon(QIcon(icon_path))
        show_action = QAction('Show', self)
        quit_action = QAction('Quit', self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage('Tomato Timer', 'The application has been minimized to the tray.', QSystemTrayIcon.Information)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    arknights_style_app = ArknightsPotatoApp()
    arknights_style_app.show()
    sys.exit(app.exec_())
