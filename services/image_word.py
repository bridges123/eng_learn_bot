import os
from PIL import Image, ImageFont, ImageDraw

font_size: int = 68
font = ImageFont.truetype('BreeSerif-Regular.ttf', size=font_size)

if not os.path.exists('images'):
    os.mkdir('images')


def create_new_image(word: str) -> str:
    image = Image.open('images/template.png')
    draw_text = ImageDraw.Draw(image)
    pos: tuple = ((image.size[0] - font_size / 2 * len(word)) / 2 - (10 - len(word)),
                  (image.size[1] - font_size) / 2 - 20)
    draw_text.text(
        xy=pos,
        text=word,
        font=font,
        fill='#FFFFFF'
    )
    path: str = f'images/{word}.png'
    image.save(path)
    return path


def get_or_create_image(word: str) -> str:
    path: str = f'images/{word}.png'
    if os.path.exists(path):
        return path
    else:
        return create_new_image(word)