from PIL import Image, ImageDraw, ImageFont
from utils.path_helper import PathHelper
from typing import Final
import os


class GIFCreator:
    __BG_COLOR: Final[str] = 'black'
    __FONT_COLOR: Final[str] = 'white'
    __FPS: Final[int] = 30
    #TODO стоит сделать путь к файлу параметром метода, а не полем класса
    __OUTPUT: Final[str] = PathHelper.join(PathHelper.get_temp_folder(), 'bot_gif.gif')


    @classmethod
    def create_gif(cls, text: str, width: int, height: int, speed: int) -> str:
        """
        Создаёт гифку из текста
        :param text: Текст, который будет отображаться в гифке
        :param width: Ширина гифки
        :param height: Высота гифки
        :param speed: Скорость движения текста
        :return: Путь к созданной гифке
        """
        #TODO стоит ли задавать возможность менять шрифт?
        font = ImageFont.truetype("arial.ttf", height - 5)

        # временное изображение для замера текста
        text_height = height
        img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(img, 'RGB')

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        frames = []

        # стартовая и конечная позиция
        x_start = width
        x_end = -int(text_width)

        y = (height - text_height) // 2
        for x in range(x_start, x_end, -speed):
            img = Image.new("RGB", (width, height), cls.__BG_COLOR)
            draw = ImageDraw.Draw(img)
            draw.text((x, y), text, font=font, fill=cls.__FONT_COLOR)
            frames.append(img)

        frames[0].save(
            cls.__OUTPUT,
            save_all=True,
            append_images=frames[1:],
            duration=int(1000 / cls.__FPS),
            loop=0
        )

        return cls.__OUTPUT

    @classmethod
    def delete_gif(cls) -> None:
        """
        Удаляет созданную гифку. Желательно вызывать этот метод после отправки гифки, чтобы не засорять систему
        """
        if os.path.exists(cls.__OUTPUT):
            os.remove(cls.__OUTPUT)
