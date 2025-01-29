import pystray
from PIL import Image, ImageDraw
import sys

image = Image.open("icon.png")
def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image
state_clock = False
state_weather = False
state_volume = False
def on_clicked(icon, item):
    global state
    state = not item.checked
    after_click()
def after_click():
    if state == True:
        print("Checked")
    else:
        print("Unchecked")
def exit():
    print("Exiting")
    sys.exit(0)
# In order for the icon to be displayed, you must provide an icon
icon = pystray.Icon("DW", image, "DisplayWidgets", 
                    menu=pystray.Menu(
    pystray.MenuItem('Clock',
                     on_clicked,
                     checked=lambda item: state_clock),
    pystray.MenuItem("Weather", 
                     on_clicked,
                     checked=lambda item: state_weather),
    pystray.MenuItem("Volume", 
                     on_clicked,
                     checked=lambda item: state_volume),
    pystray.MenuItem("Exit", exit())))
 
# To finally show you icon, call run
icon.run()