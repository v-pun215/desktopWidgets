import pystray, subprocess, os,sys
from PIL import Image
import volumeWidget, clockWidget
image = Image.open("icon.png")

state_clock = True
state_weather = False
state_volume = False

def runClock(icon, item):
    global state_clock
    state_clock = not item.checked
    if state_clock:
        clockWidget.widgets.show()
    else:
        clockWidget.widgets.hide()
def runWidget(widget):
    subprocess.Popen(['python', f'{widget}.py'])
def on_clicked():
    print("Jingalala hu hu")
def exit():
    sys.exit(0)
icon = pystray.Icon("DW", image, "DisplayWidgets", 
                    menu=pystray.Menu(
    pystray.MenuItem('Clock',
                     runClock,
                     checked=lambda item: state_clock),
    pystray.MenuItem("Weather", 
                     on_clicked,
                     checked=lambda item: state_weather),
    pystray.MenuItem("Volume", 
                     on_clicked,
                     checked=lambda item: state_volume),
    pystray.MenuItem("Exit", exit)))

icon.run()
