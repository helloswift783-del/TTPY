from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.database import DatabaseManager


class TimerPage(QWidget):
    def __init__(self, db: DatabaseManager, on_session_logged) -> None:
        super().__init__()
        self.db = db
        self.on_session_logged = on_session_logged

        self.is_running = False
        self.is_break = False
        self.remaining_seconds = self.study_seconds
        self.session_start: datetime | None = None

        self.tick = QTimer(self)
        self.tick.timeout.connect(self._on_tick)

        layout = QVBoxLayout(self)
        title = QLabel("Study Timer")
        title.setObjectName("Title")
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 64px; font-weight: 700;")
        self.status_label = QLabel("Focus Mode")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls = QHBoxLayout()
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start)
        pause_btn = QPushButton("Pause")
        pause_btn.clicked.connect(self.pause)
        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(self.stop)
        controls.addWidget(start_btn)
        controls.addWidget(pause_btn)
        controls.addWidget(stop_btn)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.status_label)
        layout.addLayout(controls)
        layout.addStretch()

        self._refresh_text()

    @property
    def study_seconds(self) -> int:
        return int(self.db.get_setting("pomodoro_study_minutes", "25")) * 60

    @property
    def break_seconds(self) -> int:
        return int(self.db.get_setting("pomodoro_break_minutes", "5")) * 60

    def start(self) -> None:
        if not self.is_running:
            self.is_running = True
            if self.session_start is None and not self.is_break:
                self.session_start = datetime.now()
            self.tick.start(1000)

    def pause(self) -> None:
        self.is_running = False
        self.tick.stop()

    def stop(self) -> None:
        self.is_running = False
        self.tick.stop()
        if self.session_start and not self.is_break:
            elapsed = max(0, self.study_seconds - self.remaining_seconds)
            if elapsed >= 60:
                self.db.add_session(elapsed // 60, self.session_start, datetime.now())
                self.on_session_logged()
        self.session_start = None
        self.is_break = False
        self.remaining_seconds = self.study_seconds
        self._refresh_text()

    def _on_tick(self) -> None:
        self.remaining_seconds -= 1
        self._refresh_text(animate=True)
        if self.remaining_seconds <= 0:
            if self.is_break:
                self.is_break = False
                self.status_label.setText("Focus Mode")
                self.remaining_seconds = self.study_seconds
                self.session_start = datetime.now()
            else:
                if self.session_start:
                    self.db.add_session(self.study_seconds // 60, self.session_start, datetime.now())
                    self.on_session_logged()
                self.session_start = None
                self.is_break = True
                self.status_label.setText("Break Mode")
                self.remaining_seconds = self.break_seconds

    def _refresh_text(self, animate: bool = False) -> None:
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")
        if animate:
            anim = QPropertyAnimation(self.timer_label, b"windowOpacity", self)
            anim.setDuration(300)
            anim.setStartValue(0.3)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.Type.OutBack)
            anim.start()
            self.timer_label._anim = anim
