from random import choice

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep
import glob
from PIL import Image
from gpiozero import Button

BUTTON_GPIO_NUMBER = 18

# see https://github.com/rm-hull/luma.examples/tree/master/examples

def convert(image_path):
    return Image.open(image_path)


def main():
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, rotate=0)
    size = [min(*device.size)] * 2
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    path_list = glob.glob('img/*.*')
    image_list = list(map(convert, path_list))

    button = Button(BUTTON_GPIO_NUMBER)

    with canvas(device) as draw:
        draw.text("Hallo Hero.")
        sleep(1)
        draw.multiline_text([0, 0], "Hallo Hero.\n Press Button!")
        button.wait_for_press()
        show_image = choice(image_list)
        background = Image.new("RGB", device.size, "white")
        background.paste(show_image.resize(size, resample=Image.LANCZOS), posn)
        previous_pressed = False
        while True:
            device.display(background.convert(device.mode))

            if button.is_pressed:
                if button.hold_time >= 10:
                    break
                show_image = choice(image_list)
        draw.multiline_text([10, 21], "Good Bye Hero...")
        sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
