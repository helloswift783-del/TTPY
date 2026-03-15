from __future__ import annotations

from datetime import date, timedelta

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.database import DatabaseManager
from app.widgets.charts import AnimatedBarChart, AnimatedLineChart


class AnalyticsPage(QWidget):
    def __init__(self, db: DatabaseManager) -> None:
        super().__init__()
        self.db = db
        layout = QVBoxLayout(self)
        title = QLabel("Progress Analytics")
        title.setObjectName("Title")
        layout.addWidget(title)

        self.daily_chart = AnimatedLineChart("Daily Study Hours (Last 14 days)")
        self.weekly_chart = AnimatedBarChart("Weekly Performance")
        self.monthly_chart = AnimatedBarChart("Monthly Progress")

        layout.addWidget(self.daily_chart, stretch=1)
        layout.addWidget(self.weekly_chart, stretch=1)
        layout.addWidget(self.monthly_chart, stretch=1)

    def refresh(self) -> None:
        daily = self.db.get_daily_hours_last_n_days(14)
        self.daily_chart.set_data(daily)

        today = date.today()
        weekly_labels = []
        weekly_values = []
        for w in range(5, -1, -1):
            end = today - timedelta(days=today.weekday()) - timedelta(days=7 * w)
            start = end - timedelta(days=7)
            weekly_labels.append(f"W{start.isocalendar().week}")
            weekly_values.append(self.db.get_total_hours_range(start, end))
        self.weekly_chart.set_data(weekly_labels, weekly_values)

        monthly_labels = []
        monthly_values = []
        for m in range(5, -1, -1):
            month_start = (today.replace(day=1) - timedelta(days=30 * m))
            month_end = month_start + timedelta(days=30)
            monthly_labels.append(month_start.strftime("%b"))
            monthly_values.append(self.db.get_total_hours_range(month_start, month_end))
        self.monthly_chart.set_data(monthly_labels, monthly_values)
