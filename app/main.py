from __future__ import annotations

import sys

from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from app.database import DatabaseManager
from app.pages.analytics import AnalyticsPage
from app.pages.dashboard import DashboardPage
from app.pages.planner import PlannerPage
from app.pages.settings_page import SettingsPage
from app.pages.timer_page import TimerPage
from app.themes import DARK_THEME, LIGHT_THEME


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("TTPY - Study Performance Tracker")
        self.resize(1300, 840)

        root = QWidget()
        main_layout = QHBoxLayout(root)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)

        self.stack = QStackedWidget()
        self.dashboard = DashboardPage(self.db)
        self.planner = PlannerPage(self.db)
        self.timer = TimerPage(self.db, self.refresh_metrics)
        self.analytics = AnalyticsPage(self.db)
        self.settings = SettingsPage(self.db, self.apply_theme, self.on_settings_saved)

        for page in [self.dashboard, self.planner, self.timer, self.analytics, self.settings]:
            self.stack.addWidget(page)

        self.nav_buttons: list[QPushButton] = []
        nav_items = [
            ("Dashboard", "🏠"),
            ("Planner", "🗓️"),
            ("Study Timer", "⏱️"),
            ("Analytics", "📊"),
            ("Settings", "⚙️"),
        ]

        for index, (name, emoji) in enumerate(nav_items):
            button = QPushButton(f"{emoji}  {name}")
            button.setProperty("nav", True)
            button.clicked.connect(lambda _, i=index: self.switch_page(i))
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addStretch()

        main_layout.addWidget(self.sidebar, stretch=1)
        main_layout.addWidget(self.stack, stretch=5)

        self.setCentralWidget(root)
        self.apply_theme(self.db.get_setting("theme", "dark"))
        self.switch_page(0, animate=False)
        self.refresh_metrics()

    def apply_theme(self, theme: str) -> None:
        self.setStyleSheet(DARK_THEME if theme == "dark" else LIGHT_THEME)

    def switch_page(self, index: int, animate: bool = True) -> None:
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        old_index = self.stack.currentIndex()
        if old_index == index:
            return

        if animate:
            old_widget = self.stack.widget(old_index)
            new_widget = self.stack.widget(index)
            width = self.stack.frameGeometry().width()
            direction = 1 if index > old_index else -1
            new_widget.move(QPoint(direction * width, 0))
            self.stack.setCurrentIndex(index)

            anim_old = QPropertyAnimation(old_widget, b"pos", self)
            anim_old.setDuration(280)
            anim_old.setStartValue(old_widget.pos())
            anim_old.setEndValue(QPoint(-direction * width, 0))
            anim_old.setEasingCurve(QEasingCurve.Type.InOutCubic)

            anim_new = QPropertyAnimation(new_widget, b"pos", self)
            anim_new.setDuration(280)
            anim_new.setStartValue(new_widget.pos())
            anim_new.setEndValue(QPoint(0, 0))
            anim_new.setEasingCurve(QEasingCurve.Type.InOutCubic)

            anim_old.start()
            anim_new.start()
            self._anim_old = anim_old
            self._anim_new = anim_new
        else:
            self.stack.setCurrentIndex(index)

        page = self.stack.currentWidget()
        if hasattr(page, "refresh"):
            page.refresh()

    def refresh_metrics(self) -> None:
        self.dashboard.refresh()
        self.analytics.refresh()

    def on_settings_saved(self) -> None:
        self.timer.remaining_seconds = self.timer.study_seconds
        self.timer._refresh_text()
        self.refresh_metrics()


def run() -> None:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
