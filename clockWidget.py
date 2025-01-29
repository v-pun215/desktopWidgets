import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QSlider, QStackedLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import *
from get_volume import GetVolume


class Layout(QWidget):
    def __init__(self):
        super().__init__()

        self.label = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnBottomHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        
        self.setGeometry(500, 500, 430, 110)  # Size and location of window
        self.center_window()
        
        self.general_layout = QVBoxLayout()  # Set a vertical layout
        self.general_layout.setSpacing(15)
        self.general_layout.setContentsMargins(15, 15, 15, 15)

        self.setLayout(self.general_layout)
        self.volume = GetVolume()  # The volume file we made earlier
        self.make_widget()
        self.general_layout.addStretch() # Fill any extra space in the window.

        self.show()
    def center_window(self):
            # Get the screen geometry
            screen_geometry = QApplication.primaryScreen().availableGeometry()

            # Calculate the center position
            center_point = screen_geometry.center()

            # Calculate the position of the window's top-left corner
            x = center_point.x() - self.width() // 2
            y = center_point.y() - self.height() // 2

            # Move the window to the calculated position
            self.move(x, y)

    def make_widget(self):
        self.label = QLabel(self)  # All widgets are Labels
        self.label.setFixedSize(430, 110)  # Set the size of Label
        self.label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.label.setStyleSheet('QWidget{background: '
                                 'rgba(255,255,255, .4);'
                                 ' padding: 20px; border-radius: 30px; webkit-backdrop-filter: blur(5px);}')
        # Do some styling to said widget
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_widget()

    def volume_widget(self): 
        # Sliders are a little finicky so we do some extra formatting
        s_layout = QStackedLayout()
        s_layout.setSpacing(0)
        s_layout.setContentsMargins(0, 0, 0, 0)
        s_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        slider = QSlider(self)
        centered_frame = QFrame()
        centered_frame.setLayout(QVBoxLayout())
        centered_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        centered_frame.layout().addWidget(slider)

        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setMinimum(int(self.volume.audio_range[0] * 100))
        slider.setMaximum(int(self.volume.audio_range[1] * 100))
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(100)
        slider.setValue(int(self.volume.current_volume * 100))

        slider.setFixedSize(250, 40)
        slider.valueChanged.connect(self.update_volume_on_slider_change)  # Connect the slider to our volume file

        centered_frame.layout().addWidget(slider)

        self.label.setText(f"""
        <html>
            <p style="font-size: 30px; white-space: pre;">🔇{"&#9;" * 4}🔊</p>
        </html>
        """)

        s_layout.addWidget(self.label)
        s_layout.addWidget(centered_frame)
        s_layout.setCurrentIndex(1)

        self.general_layout.addLayout(s_layout)  # add it to the layout

    def update_volume_on_slider_change(self, value):
        self.volume.set_volume(value / 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widgets = Layout()
    sys.exit(app.exec())
else:
    app = QApplication(sys.argv)
    widgets = Layout()

def runApp():
    app = QApplication(sys.argv)
    widgets = Layout()
    sys.exit(app.exec())
def showApp():
    widgets = Layout()
    widgets.show()
def hideApp():
    widgets = Layout()
    widgets.hide()