from __future__ import annotations

from PyQt6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter


class AnimatedBarChart(QChartView):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.chart_obj = QChart()
        self.chart_obj.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart_obj.setTitle(title)
        self.setChart(self.chart_obj)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def set_data(self, categories: list[str], values: list[float]) -> None:
        self.chart_obj.removeAllSeries()
        self.chart_obj.removeAxis(self.chart_obj.axisX()) if self.chart_obj.axisX() else None
        self.chart_obj.removeAxis(self.chart_obj.axisY()) if self.chart_obj.axisY() else None

        bar_set = QBarSet("Hours")
        bar_set.append(values)
        series = QBarSeries()
        series.append(bar_set)
        self.chart_obj.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%.1f")
        axis_y.setRange(0, max(values + [1.0]) + 1)

        self.chart_obj.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart_obj.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)


class AnimatedLineChart(QChartView):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.chart_obj = QChart()
        self.chart_obj.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart_obj.setTitle(title)
        self.setChart(self.chart_obj)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def set_data(self, points: list[tuple[str, float]]) -> None:
        self.chart_obj.removeAllSeries()
        self.chart_obj.removeAxis(self.chart_obj.axisX()) if self.chart_obj.axisX() else None
        self.chart_obj.removeAxis(self.chart_obj.axisY()) if self.chart_obj.axisY() else None

        line = QLineSeries()
        for i, (_, value) in enumerate(points):
            line.append(QPointF(float(i), value))

        self.chart_obj.addSeries(line)

        axis_x = QValueAxis()
        axis_x.setRange(0, max(len(points) - 1, 1))
        axis_x.setTickCount(min(len(points), 10))

        axis_y = QValueAxis()
        axis_y.setRange(0, max([v for _, v in points] + [1.0]) + 1)
        axis_y.setLabelFormat("%.1f h")

        self.chart_obj.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart_obj.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        line.attachAxis(axis_x)
        line.attachAxis(axis_y)
