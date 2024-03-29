from random import choice

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep
from pathlib import Path
from PIL import Image
from gpiozero import Button

BUTTON_GPIO_NUMBER = 18
BACKGROUND_COLOR = "white"

# see https://github.com/rm-hull/luma.examples/tree/master/examples

def convert(image_path):
    return Image.open(image_path)


def display_random_image(image_list, device, button, posn):
    show_image = choice(image_list)
    background = Image.new("RGB", device.size, BACKGROUND_COLOR)
    background.paste(show_image, posn)
    device.display(background.convert(device.mode))

def main():
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, rotate=0)
    size = [min(*device.size)] * 2
    # 描画位置の計算
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    # 終了時処理の登録
    def sig_handler(signum, frame) -> None:
        device.cleanup()
        sys.exit(1)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    current_dir = Path(__file__).parent
    path_list = current_dir.glob('img/*.*')
    image_list = list(map(convert, path_list))

    button = Button(BUTTON_GPIO_NUMBER)

    with canvas(device) as draw:
        while True:
            while button.is_pressed != True:
                display_random_image(image_list, device, button, posn)
                sleep(0.1)
            display_random_image(image_list, device, button, posn)
            button.wait_for_release()
            button.wait_for_press()
            button.wait_for_release()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
