from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database import DatabaseManager


class PlannerPage(QWidget):
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self, db: DatabaseManager) -> None:
        super().__init__()
        self.db = db
        layout = QVBoxLayout(self)
        title = QLabel("Study Planner")
        title.setObjectName("Title")
        layout.addWidget(title)

        controls = QHBoxLayout()
        self.day_combo = QComboBox()
        self.day_combo.addItems(self.DAYS)
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Topic")
        self.hours_input = QDoubleSpinBox()
        self.hours_input.setRange(0.5, 12)
        self.hours_input.setSingleStep(0.5)
        self.hours_input.setValue(1.0)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_entry)
        save_btn = QPushButton("Save Planner")
        save_btn.clicked.connect(self.save_to_db)

        for w in [self.day_combo, self.subject_input, self.topic_input, self.hours_input, add_btn, save_btn]:
            controls.addWidget(w)

        layout.addLayout(controls)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Day", "Subject", "Topic", "Target Hours"])
        self.table.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.viewport().setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)
        self.table.setDefaultDropAction(Qt.DropAction.MoveAction)
        layout.addWidget(self.table, stretch=1)

        self.load_from_db()

    def add_entry(self) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        values = [
            self.day_combo.currentText(),
            self.subject_input.text().strip() or "General Study",
            self.topic_input.text().strip() or "-",
            f"{self.hours_input.value():.1f}",
        ]
        for col, value in enumerate(values):
            self.table.setItem(row, col, QTableWidgetItem(value))

    def save_to_db(self) -> None:
        self.db.clear_planner()
        for row in range(self.table.rowCount()):
            day = self.DAYS.index(self.table.item(row, 0).text())
            subject = self.table.item(row, 1).text()
            topic = self.table.item(row, 2).text()
            hours = float(self.table.item(row, 3).text())
            self.db.save_planner_entry(day, subject, topic, hours, row)

    def load_from_db(self) -> None:
        entries = self.db.get_planner_entries()
        self.table.setRowCount(0)
        for item in entries:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [self.DAYS[item["day_of_week"]], item["subject"], item["topic"], f'{item["target_hours"]:.1f}']
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(value))
