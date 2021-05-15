from random import choice

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep
import glob
from PIL import Image
from gpiozero import Button

BUTTON_GPIO_NUMBER = 18
BACKGROUND_COLOR = "white"

# see https://github.com/rm-hull/luma.examples/tree/master/examples

def convert(image_path):
    return Image.open(image_path)


def loop_image_until_press(posn):
    while button.is_pressed != True:
        show_image = choice(image_list)
        background = Image.new("RGB", device.size, BACKGROUND_COLOR)
        background.paste(show_image, posn)
        device.display(background.convert(device.mode))
        sleep(0.1)

def main():
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, rotate=0)
    size = [min(*device.size)] * 2
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    path_list = glob.glob('img/*.*')
    image_list = list(map(convert, path_list))

    button = Button(BUTTON_GPIO_NUMBER)

    with canvas(device) as draw:
    	while True:
            loop_image_until_press(posn)
            show_image = choice(image_list)
            background = Image.new("RGB", device.size, BACKGROUND_COLOR)
            background.paste(show_image.resize(size, resample=Image.LANCZOS), posn)
            device.display(background.convert(device.mode))
            button.wait_for_press()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
