DARK_THEME = """
QMainWindow, QWidget { background-color: #12151f; color: #e9edf5; font-family: 'DejaVu Sans'; }
QFrame#Sidebar { background-color: #0f111a; border-right: 1px solid #252a3a; }
QPushButton { background-color: #1c2233; border: 1px solid #2d3650; padding: 8px 12px; border-radius: 10px; }
QPushButton:hover { background-color: #2a3350; border-color: #5d7be5; }
QPushButton:pressed { background-color: #3a4470; }
QPushButton[nav='true'] { text-align: left; padding: 12px; border-radius: 12px; }
QPushButton[active='true'] { background-color: #4058a8; border-color: #8096eb; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget {
    background-color: #1b2030; border: 1px solid #2d3650; border-radius: 8px; padding: 6px;
}
QHeaderView::section { background-color: #111826; color: #d3dcf7; border: none; padding: 6px; }
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#CardValue { font-size: 28px; font-weight: 700; }
QProgressBar { border: 1px solid #2d3650; border-radius: 8px; text-align: center; height: 18px; }
QProgressBar::chunk { background-color: #5d7be5; border-radius: 7px; }
QFrame#Card { background-color: #181d2c; border: 1px solid #2d3650; border-radius: 14px; }
"""

LIGHT_THEME = """
QMainWindow, QWidget { background-color: #f2f4f8; color: #1f2737; font-family: 'DejaVu Sans'; }
QFrame#Sidebar { background-color: #e7ebf3; border-right: 1px solid #c4cedf; }
QPushButton { background-color: #ffffff; border: 1px solid #c4cedf; padding: 8px 12px; border-radius: 10px; }
QPushButton:hover { background-color: #eaf0ff; border-color: #617ee6; }
QPushButton:pressed { background-color: #dae4ff; }
QPushButton[nav='true'] { text-align: left; padding: 12px; border-radius: 12px; }
QPushButton[active='true'] { background-color: #5d7be5; color: white; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget {
    background-color: #ffffff; border: 1px solid #c4cedf; border-radius: 8px; padding: 6px;
}
QHeaderView::section { background-color: #dfe6f4; color: #1f2737; border: none; padding: 6px; }
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#CardValue { font-size: 28px; font-weight: 700; }
QProgressBar { border: 1px solid #c4cedf; border-radius: 8px; text-align: center; height: 18px; }
QProgressBar::chunk { background-color: #5d7be5; border-radius: 7px; }
QFrame#Card { background-color: #ffffff; border: 1px solid #c4cedf; border-radius: 14px; }
"""
