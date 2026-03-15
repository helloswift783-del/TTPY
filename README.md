diff --git a/README.md b/README.md
index 45e85ad68925ce1248e1d435babe0b4a4366185d..c861cf23c6aac6fc2a092bc7bcd9c80b93ff83ab 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,72 @@
-# Tracking-app
-created a app for tracking the productivity .
+# TTPY (Tracking-app)
+
+TTPY is a desktop study performance tracker for Linux built with **Python + PyQt6**.
+
+## Features
+
+- **Dashboard**
+  - Daily, weekly, and monthly study totals
+  - Animated progress bars
+  - Animated weekly + monthly charts
+  - Motivational quote, streak counter, and productivity score
+- **Study Planner**
+  - Add weekly schedule entries (subject, topic, target hours)
+  - Drag-and-drop row reordering
+  - Persist planner data locally in SQLite
+- **Study Timer**
+  - Built-in Pomodoro timer (focus + break)
+  - Start/Pause/Stop controls
+  - Smooth timer label updates
+  - Auto-save completed focus sessions
+- **Analytics**
+  - Daily line chart
+  - Weekly and monthly bar charts
+  - Chart animations on refresh
+- **Settings**
+  - Configure Pomodoro durations
+  - Toggle dark/light theme
+  - Set weekly hour goal
+
+## Project Structure
+
+```text
+.
+├── main.py
+├── requirements.txt
+└── app
+    ├── main.py
+    ├── database.py
+    ├── themes.py
+    ├── pages
+    │   ├── dashboard.py
+    │   ├── planner.py
+    │   ├── timer_page.py
+    │   ├── analytics.py
+    │   └── settings_page.py
+    └── widgets
+        └── charts.py
+```
+
+## Install (Linux)
+
+```bash
+python3 -m venv .venv
+source .venv/bin/activate
+pip install -r requirements.txt
+```
+
+## Run
+
+```bash
+python main.py
+```
+
+## Data Storage
+
+- SQLite DB file is created locally as `tt_py.db` in the project folder.
+- Study sessions, planner entries, and settings are saved automatically.
+
+## Notes
+
+- The app is modular and class-based (each page/component has its own class).
+- The UI is responsive using Qt layouts and styled with dark/light themes.
