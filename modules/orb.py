import sys
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QMenu
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QRadialGradient, QColor, QPen, QAction

COLORS = {
    "idle":      {"core": "#FF6000", "mid": "#CC3000", "glow": "#FF2200", "ring": "#FF4400"},
    "listening": {"core": "#FFB300", "mid": "#FF6600", "glow": "#FF4400", "ring": "#FFAA00"},
    "thinking":  {"core": "#FF8C00", "mid": "#AA4400", "glow": "#882200", "ring": "#FF6600"},
    "speaking":  {"core": "#FFFFFF", "mid": "#FFD700", "glow": "#FF6600", "ring": "#FFD700"},
}

SPEEDS = {
    "idle":      {"pulse": 0.015, "rotate": 0.3},
    "listening": {"pulse": 0.05,  "rotate": 1.2},
    "thinking":  {"pulse": 0.02,  "rotate": 0.8},
    "speaking":  {"pulse": 0.07,  "rotate": 2.0},
}

class OrbSignals(QObject):
    state_changed = pyqtSignal(str)
    listen_triggered = pyqtSignal()
    quit_triggered = pyqtSignal()

class OrbWidget(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.state = "idle"
        self.pulse = 0.0
        self.pulse_dir = 1
        self.angle = 0.0
        self.signals = signals
        self.signals.state_changed.connect(self._on_state_changed)
        self._init_window()

        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.start(30)

    def _init_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(120, 120)

        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 140, 20)

    def _on_state_changed(self, state):
        self.state = state

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.signals.listen_triggered.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            menu = QMenu(self)
            listen_action = QAction("Listen", self)
            quit_action = QAction("Quit", self)
            listen_action.triggered.connect(self.signals.listen_triggered.emit)
            quit_action.triggered.connect(self.signals.quit_triggered.emit)
            menu.addAction(listen_action)
            menu.addAction(quit_action)
            menu.exec(event.globalPosition().toPoint())

    def _animate(self):
        speed = SPEEDS[self.state]
        self.pulse += speed["pulse"] * self.pulse_dir
        if self.pulse >= 1.0:
            self.pulse_dir = -1
        elif self.pulse <= 0.0:
            self.pulse_dir = 1

        self.angle = (self.angle + speed["rotate"]) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        colors = COLORS[self.state]
        cx, cy = 60, 60
        base_radius = 28 + 6 * self.pulse

        painter.setBrush(QColor(0, 0, 0, 180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - 54), int(cy - 54), 108, 108)

        outer_glow = QRadialGradient(cx, cy, 54)
        glow_color = QColor(colors["glow"])
        glow_color.setAlpha(int(60 + 80 * self.pulse))
        outer_glow.setColorAt(0.6, glow_color)
        outer_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(outer_glow)
        painter.drawEllipse(int(cx - 54), int(cy - 54), 108, 108)

        pen = QPen(QColor(colors["ring"]))
        pen.setWidth(2)
        ring_color = QColor(colors["ring"])
        ring_color.setAlpha(int(120 + 100 * self.pulse))
        pen.setColor(ring_color)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for i in range(3):
            offset = self.angle + i * 120
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(offset)
            painter.drawArc(-40, -40, 80, 80, 0, 120 * 16)
            painter.restore()

        inner_color = QColor(colors["ring"])
        inner_color.setAlpha(int(80 + 60 * self.pulse))
        pen2 = QPen(inner_color)
        pen2.setWidth(1)
        painter.setPen(pen2)
        for i in range(3):
            offset = -self.angle + i * 120
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(offset)
            painter.drawArc(-28, -28, 56, 56, 0, 100 * 16)
            painter.restore()

        core = QRadialGradient(cx, cy, base_radius)
        core.setColorAt(0.0, QColor("#FFFFFF"))
        core.setColorAt(0.2, QColor(colors["core"]))
        core.setColorAt(0.6, QColor(colors["mid"]))
        core.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(core)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(cx - base_radius), int(cy - base_radius),
            int(base_radius * 2), int(base_radius * 2)
        )

        hot = QRadialGradient(cx, cy, 8)
        hot.setColorAt(0.0, QColor(255, 255, 255, 255))
        hot.setColorAt(0.5, QColor(255, 220, 100, 180))
        hot.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(hot)
        painter.drawEllipse(cx - 8, cy - 8, 16, 16)

orb_signals = OrbSignals()

def set_state(state: str):
    orb_signals.state_changed.emit(state)