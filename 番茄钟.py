import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon

class ArknightsPotatoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置窗口标题为Tomato Timer
        self.setWindowTitle('Tomato Timer')
        # 设置窗口位置为（100，100），宽为400，高为200
        self.setGeometry(100, 100, 400, 200)

        # 初始化时间变量
        self.time_left = 25 * 60
        self.break_time = 10 * 60
        self.paused = False
        self.on_break = False

        # 初始化布局
        self.layout = QVBoxLayout()

        # 设置标签，显示剩余时间
        self.label_timer = QLabel(self.format_time(self.time_left), self)
        font = self.label_timer.font()
        font.setFamily("幼圆")
        font.setPointSize(40)
        self.label_timer.setFont(font)
        self.label_timer.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_timer)

        # 初始化进度条
        self.progress_bar = QProgressBar(self)
        # 设置进度条的最大值
        self.progress_bar.setMaximum(self.time_left)
        # 设置进度条的初始值
        self.progress_bar.setValue(self.time_left)
        # 将进度条添加到布局中
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
        # 如果定时器没有暂停
        if not self.on_break:
            # 暂停状态设置为False
            self.paused = False
            # 开始按钮设置为不可用
            self.start_button.setEnabled(False)
            # 暂停按钮设置为可用
            self.pause_button.setEnabled(True)
            # 开始计时，每隔1000毫秒调用一次回调函数
            self.timer.start(1000)
        else:
            # 开始休息计时
            self.start_break_timer()

    def start_break_timer(self):
        # 设置暂停状态为False
        self.paused = False
        # 设置on_break状态为True
        self.on_break = True
        # 设置剩余时间为break_time
        self.time_left = self.break_time
        # 设置label_timer的文本为格式化后的time_left
        self.label_timer.setText(self.format_time(self.time_left))
        # 设置进度条的最大值为time_left
        self.progress_bar.setMaximum(self.time_left)
        # 设置进度条的值为time_left
        self.progress_bar.setValue(self.time_left)
        # 设置start_button不可用
        self.start_button.setEnabled(False)
        # 设置pause_button可用
        self.pause_button.setEnabled(True)
        # 启动定时器，每隔1000毫秒执行一次
        self.timer.start(1000)

    def pause_timer(self):
        # 暂停计时器
        self.paused = True
        # 停止计时器
        self.timer.stop()
        # 启用开始按钮
        self.start_button.setEnabled(True)
        # 禁用暂停按钮
        self.pause_button.setEnabled(False)

    # 重置计时器函数
    def reset_timer(self):
        # 停止计时器
        self.timer.stop()
        # 如果不是暂停状态
        if not self.on_break:
            # 将剩余时间设置为25分钟
            self.time_left = 25 * 60
        else:
            # 如果是暂停状态，将剩余时间设置为休息时间
            self.time_left = self.break_time
            # 将暂停状态设置为False
            self.on_break = False
        # 将计时器显示的时间设置为剩余时间
        self.label_timer.setText(self.format_time(self.time_left))
        # 将进度条的最大值设置为剩余时间
        self.progress_bar.setMaximum(self.time_left)
        # 将进度条的当前值设置为剩余时间
        self.progress_bar.setValue(self.time_left)
        # 将开始按钮设置为可用状态
        self.start_button.setEnabled(True)
        # 将暂停按钮设置为不可用状态
        self.pause_button.setEnabled(False)
        # 将暂停状态设置为False
        self.paused = False

    def update_timer(self):
        # 如果计时器没有结束
        if self.time_left > 0:
            # 计时器减1
            self.time_left -= 1
            # 更新计时器标签
            self.label_timer.setText(self.format_time(self.time_left))
            # 更新进度条
            self.progress_bar.setValue(self.time_left)
        else:
            # 如果计时器结束，停止计时器
            self.timer.stop()
            # 如果不是休息时间
            if not self.on_break:
                # 更新计时器标签
                self.label_timer.setText("Time's up! Take a break!")
                # 启用开始按钮
                self.start_button.setEnabled(True)
                # 禁用暂停按钮
                self.pause_button.setEnabled(False)
                # 暂停状态设置为False
                self.paused = False
                # 番茄钟数量加1
                self.tomato_count += 1
                # 更新番茄钟标签
                self.label_count.setText(f'Tomato Count: {self.tomato_count}')
            else:
                # 如果是休息时间
                # 更新计时器标签
                self.label_timer.setText("Break's over! Start working!")
                # 开始计时器
                self.start_timer()

    def format_time(self, seconds):
        #将秒数格式化为``mm:ss``格式
        minutes, seconds = divmod(seconds, 60)
        return f'{minutes:02d}:{seconds:02d}'

    def create_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置图标路径
        icon_path = 'icon(path)'
        # 设置图标
        self.tray_icon.setIcon(QIcon(icon_path))
        # 创建显示图标动作
        show_action = QAction('Show', self)
        # 创建退出图标动作
        quit_action = QAction('Quit', self)
        # 连接显示图标动作的触发器
        show_action.triggered.connect(self.show)
        # 连接退出图标动作的触发器
        quit_action.triggered.connect(self.close)
        # 创建托盘菜单
        tray_menu = QMenu()
        # 将显示图标动作添加到托盘菜单中
        tray_menu.addAction(show_action)
        # 将退出图标动作添加到托盘菜单中
        tray_menu.addAction(quit_action)
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        # 显示托盘图标
        self.tray_icon.show()

    def closeEvent(self, event):
        #重写closeEvent函数，当点击关闭按钮时，隐藏窗口，但是不关闭应用，同时显示托盘图标，并显示信息。
        event.ignore()
        self.hide()
        self.tray_icon.showMessage('Tomato Timer', 'The application has been minimized to the tray.', QSystemTrayIcon.Information)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    arknights_style_app = ArknightsPotatoApp()
    arknights_style_app.show()
    sys.exit(app.exec_())
