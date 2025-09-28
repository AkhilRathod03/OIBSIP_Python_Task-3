
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSlider, QCheckBox, QProgressBar,
    QFrame, QGraphicsDropShadowEffect, QSplitter
)
from PySide6.QtGui import QColor, QIcon, QPainter, QFont, QFontDatabase, QPixmap, QImage
from PySide6.QtCore import Qt, QSize, Property, QPropertyAnimation, QEasingCurve, QTimer
import password_logic
import os

# --- Custom Toggle Switch ---
class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self._bg_color = QColor("#555")
        self._circle_color = QColor("#DDD")
        self._active_color = QColor("#007acc")
        
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(200)
        
        self.stateChanged.connect(self.start_transition)

    @Property(int)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.setStartValue(self.circle_position)
        if value:
            self.animation.setEndValue(self.width() - 23)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        rect = self.contentsRect()
        h = rect.height()
        w = 40
        
        p.setBrush(self._bg_color)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, (h/2)-10, w, 20, 10, 10)
        
        p.setBrush(self._circle_color)
        if self.isChecked():
            p.setBrush(self._active_color)
        
        p.drawEllipse(self._circle_position, (h/2)-8, 16, 16)
        p.end()

    def sizeHint(self):
        return QSize(45, 25)

# --- Main GUI Application ---
class GuiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.light_theme_path = os.path.join(self.current_dir, "light_theme.qss")
        self.dark_theme_path = os.path.join(self.current_dir, "dark_theme.qss")

        self.sun_icon = self.create_icon("#f9d71c", "circle")
        self.moon_icon = self.create_icon("#a0a0a0", "circle")
        self.copy_icon = self.create_icon("#a0a0a0", "copy")
        self.menu_icon = self.create_icon("#a0a0a0", "menu")

        self.setWindowTitle("Modern Password Generator")
        self.setMinimumSize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.create_options_panel()
        self.create_main_panel()

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.options_panel)
        self.splitter.addWidget(self.main_panel)
        self.splitter.setSizes([250, 550])
        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, False)
        self.main_layout.addWidget(self.splitter)

        self.is_dark_theme = True
        self.load_stylesheet(self.dark_theme_path)
        
        self.generate_and_display()

    def create_icon(self, color, shape="circle"):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = painter.pen()
        pen.setColor(QColor(color))
        pen.setWidth(2)
        painter.setPen(pen)

        if shape == "copy":
             painter.drawRect(8, 5, 13, 16)
             painter.drawRect(12, 2, 13, 16)
        elif shape == "circle":
            painter.drawEllipse(6, 6, 20, 20)
        elif shape == "menu":
            painter.drawLine(6, 8, 26, 8)
            painter.drawLine(6, 16, 26, 16)
            painter.drawLine(6, 24, 26, 24)
            
        painter.end()
        return QIcon(pixmap)

    def create_options_panel(self):
        self.options_panel = QFrame()
        self.options_panel.setObjectName("OptionsPanel")
        self.options_layout = QVBoxLayout(self.options_panel)
        self.options_layout.setContentsMargins(15, 15, 15, 15)
        self.options_layout.setSpacing(15)
        
        title = QLabel("Properties")
        title.setObjectName("OptionsTitle")
        title.setAlignment(Qt.AlignCenter)
        self.options_layout.addWidget(title)

        self.len_var = 18
        len_label = QLabel(f"Password Length: {self.len_var}")
        self.options_layout.addWidget(len_label)
        len_slider = QSlider(Qt.Horizontal)
        len_slider.setRange(4, 64)
        len_slider.setValue(self.len_var)
        len_slider.valueChanged.connect(lambda v: (
            setattr(self, 'len_var', v),
            len_label.setText(f"Password Length: {v}"),
            self.generate_and_display()
        ))
        self.options_layout.addWidget(len_slider)

        self.upper_var = self.create_toggle("Include Uppercase (A-Z)", True)
        self.lower_var = self.create_toggle("Include Lowercase (a-z)", True)
        self.numbers_var = self.create_toggle("Include Numbers (0-9)", True)
        self.symbols_var = self.create_toggle("Include Symbols (!@#$)", True)
        self.exclude_similar_var = self.create_toggle("Exclude Similar (O, 0, l, 1)", False)

        self.options_layout.addStretch()

    def create_toggle(self, text, checked=False):
        toggle_layout = QHBoxLayout()
        label = QLabel(text)
        switch = ToggleSwitch()
        switch.setChecked(checked)
        switch.stateChanged.connect(self.generate_and_display)
        toggle_layout.addWidget(label)
        toggle_layout.addStretch()
        toggle_layout.addWidget(switch)
        self.options_layout.addLayout(toggle_layout)
        return switch

    def create_main_panel(self):
        self.main_panel = QFrame()
        main_panel_layout = QVBoxLayout(self.main_panel)
        main_panel_layout.setAlignment(Qt.AlignCenter)

        # --- Top bar with Title and Toggles ---
        top_bar_layout = QHBoxLayout()
        
        self.panel_toggle_button = QPushButton(self.menu_icon, "")
        self.panel_toggle_button.setObjectName("ThemeButton") # Use same style as theme button
        self.panel_toggle_button.setCursor(Qt.PointingHandCursor)
        self.panel_toggle_button.clicked.connect(self.toggle_options_panel)
        self.panel_toggle_button.setFixedSize(40, 40)
        self.panel_toggle_button.setIconSize(QSize(28, 28))
        top_bar_layout.addWidget(self.panel_toggle_button)

        top_bar_layout.addStretch()
        self.theme_button = QPushButton(self.moon_icon, "")
        self.theme_button.setObjectName("ThemeButton")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setIconSize(QSize(28, 28))
        top_bar_layout.addWidget(self.theme_button)
        main_panel_layout.addLayout(top_bar_layout)

        # --- Main Title ---
        title_label = QLabel("Modern Password Generator")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_panel_layout.addWidget(title_label)

        main_panel_layout.addStretch(1)

        # --- Password Card ---
        card = QFrame()
        card.setObjectName("PasswordCard")
        card.setMinimumSize(450, 150)
        card.setMaximumSize(600, 200)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        self.password_display = QLineEdit("Generating...")
        self.password_display.setObjectName("PasswordDisplay")
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignCenter)
        
        copy_button = QPushButton(self.copy_icon, "")
        copy_button.setObjectName("CopyButton")
        copy_button.setCursor(Qt.PointingHandCursor)
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setFixedSize(45, 45)
        copy_button.setIconSize(QSize(32, 32))
        
        display_layout = QHBoxLayout()
        display_layout.addWidget(self.password_display)
        display_layout.addWidget(copy_button)
        card_layout.addLayout(display_layout)

        self.strength_label = QLabel("Strength")
        self.strength_label.setObjectName("StrengthLabel")
        card_layout.addWidget(self.strength_label, 0, Qt.AlignLeft)
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(8)
        self.strength_bar.setTextVisible(False)
        card_layout.addWidget(self.strength_bar)

        self.copied_label = QLabel("Copied to clipboard!")
        self.copied_label.setObjectName("CopiedLabel")
        self.copied_label.setAlignment(Qt.AlignCenter)
        self.copied_label.hide()
        card_layout.addWidget(self.copied_label)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        card.setGraphicsEffect(shadow)
        
        main_panel_layout.addWidget(card)
        
        generate_button = QPushButton("Generate Password")
        generate_button.setMinimumHeight(50)
        generate_button.clicked.connect(self.generate_and_display)
        main_panel_layout.addWidget(generate_button)
        main_panel_layout.addStretch(2)

    def generate_and_display(self, *args):
        password, error = password_logic.generate_password(
            length=self.len_var,
            use_upper=self.upper_var.isChecked(),
            use_lower=self.lower_var.isChecked(),
            use_numbers=self.numbers_var.isChecked(),
            use_symbols=self.symbols_var.isChecked(),
            exclude_similar=self.exclude_similar_var.isChecked()
        )
        
        if error:
            self.password_display.setText(error)
            self.update_strength_meter("")
        else:
            self.password_display.setText(password)
            self.update_strength_meter(password)

    def update_strength_meter(self, password):
        strength, score = password_logic.check_strength(password)
        self.strength_bar.setValue(score)
        self.strength_label.setText(f"Strength: {strength}")
        
        self.strength_bar.setProperty("strength", strength)
        self.style().unpolish(self.strength_bar)
        self.style().polish(self.strength_bar)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.password_display.text())
        self.copied_label.show()
        QTimer.singleShot(2000, self.copied_label.hide)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.load_stylesheet(self.dark_theme_path)
            self.theme_button.setIcon(self.moon_icon)
        else:
            self.load_stylesheet(self.light_theme_path)
            self.theme_button.setIcon(self.sun_icon)

    def toggle_options_panel(self):
        if self.options_panel.isVisible():
            self.options_panel.hide()
        else:
            self.options_panel.show()

    def load_stylesheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Stylesheet not found at: {path}")

def run_gui():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = GuiApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
