from __future__ import annotations

from datetime import date, timedelta

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QProgressBar, QVBoxLayout, QWidget

from app.database import DatabaseManager
from app.widgets.charts import AnimatedBarChart


class DashboardPage(QWidget):
    def __init__(self, db: DatabaseManager) -> None:
        super().__init__()
        self.db = db

        layout = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setObjectName("Title")
        layout.addWidget(title)

        self.cards_layout = QGridLayout()
        layout.addLayout(self.cards_layout)

        self.day_value, self.day_bar = self._add_card(0, "Today")
        self.week_value, self.week_bar = self._add_card(1, "This Week")
        self.month_value, self.month_bar = self._add_card(2, "This Month")

        self.quote = QLabel('"Consistency beats intensity."')
        layout.addWidget(self.quote)

        self.week_chart = AnimatedBarChart("Weekly Study Hours")
        self.month_chart = AnimatedBarChart("Monthly Study Hours")
        layout.addWidget(self.week_chart, stretch=1)
        layout.addWidget(self.month_chart, stretch=1)

    def _add_card(self, column: int, title: str) -> tuple[QLabel, QProgressBar]:
        card = QFrame()
        card.setObjectName("Card")
        box = QVBoxLayout(card)
        label = QLabel(title)
        value = QLabel("0.0 h")
        value.setObjectName("CardValue")
        progress = QProgressBar()
        progress.setRange(0, 100)
        box.addWidget(label)
        box.addWidget(value)
        box.addWidget(progress)
        self.cards_layout.addWidget(card, 0, column)
        return value, progress

    def _animate_progress(self, bar: QProgressBar, value: int) -> None:
        anim = QPropertyAnimation(bar, b"value", self)
        anim.setDuration(700)
        anim.setStartValue(bar.value())
        anim.setEndValue(value)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        bar._anim = anim

    def refresh(self) -> None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        day_hours = self.db.get_total_hours_for_date(today)
        week_hours = self.db.get_total_hours_range(week_start, today + timedelta(days=1))
        month_hours = self.db.get_total_hours_range(month_start, today + timedelta(days=1))

        self.day_value.setText(f"{day_hours:.2f} h")
        self.week_value.setText(f"{week_hours:.2f} h")
        self.month_value.setText(f"{month_hours:.2f} h")

        weekly_goal = float(self.db.get_setting("weekly_goal_hours", "20"))
        self._animate_progress(self.day_bar, min(int((day_hours / max(weekly_goal / 7, 1)) * 100), 100))
        self._animate_progress(self.week_bar, min(int((week_hours / max(weekly_goal, 1)) * 100), 100))
        self._animate_progress(self.month_bar, min(int((month_hours / max(weekly_goal * 4, 1)) * 100), 100))

        week_points = []
        day_labels = []
        day_values = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_labels.append(day.strftime("%a"))
            day_values.append(self.db.get_total_hours_for_date(day))
            week_points.append((day.strftime("%a"), day_values[-1]))

        month_points = []
        month_labels = []
        month_values = []
        for i in range(3, -1, -1):
            start = (today.replace(day=1) - timedelta(days=30 * i))
            end = start + timedelta(days=30)
            month_labels.append(start.strftime("%b"))
            month_values.append(self.db.get_total_hours_range(start, end))
            month_points.append((month_labels[-1], month_values[-1]))

        self.week_chart.set_data(day_labels, day_values)
        self.month_chart.set_data(month_labels, month_values)

        streak = self.db.get_study_streak()
        productivity = min(int((week_hours / max(weekly_goal, 1)) * 100), 100)
        self.quote.setText(
            f'"Consistency beats intensity."  🔥 Streak: {streak} day(s) | Productivity Score: {productivity}%'
        )
