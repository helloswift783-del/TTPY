from __future__ import annotations

from PyQt6.QtWidgets import QComboBox, QFormLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget

from app.database import DatabaseManager


class SettingsPage(QWidget):
    def __init__(self, db: DatabaseManager, on_theme_change, on_settings_saved) -> None:
        super().__init__()
        self.db = db
        self.on_theme_change = on_theme_change
        self.on_settings_saved = on_settings_saved

        layout = QVBoxLayout(self)
        title = QLabel("Settings")
        title.setObjectName("Title")
        layout.addWidget(title)

        form = QFormLayout()
        self.study_spin = QSpinBox()
        self.study_spin.setRange(10, 90)
        self.study_spin.setValue(int(self.db.get_setting("pomodoro_study_minutes", "25")))

        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 30)
        self.break_spin.setValue(int(self.db.get_setting("pomodoro_break_minutes", "5")))

        self.goal_spin = QSpinBox()
        self.goal_spin.setRange(1, 80)
        self.goal_spin.setValue(int(float(self.db.get_setting("weekly_goal_hours", "20"))))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        idx = self.theme_combo.findText(self.db.get_setting("theme", "dark"))
        self.theme_combo.setCurrentIndex(max(idx, 0))

        form.addRow("Pomodoro study minutes", self.study_spin)
        form.addRow("Pomodoro break minutes", self.break_spin)
        form.addRow("Weekly study goal (hours)", self.goal_spin)
        form.addRow("Theme", self.theme_combo)

        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save)

        layout.addLayout(form)
        layout.addWidget(save_btn)
        layout.addStretch()

    def save(self) -> None:
        self.db.set_setting("pomodoro_study_minutes", str(self.study_spin.value()))
        self.db.set_setting("pomodoro_break_minutes", str(self.break_spin.value()))
        self.db.set_setting("weekly_goal_hours", str(self.goal_spin.value()))
        self.db.set_setting("theme", self.theme_combo.currentText())
        self.on_theme_change(self.theme_combo.currentText())
        self.on_settings_saved()
