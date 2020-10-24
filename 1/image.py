from PIL import Image, ImageDraw, ImageFont

im = Image.open('C:/Users/sheli/PycharmProjects/CoronaBot/chel.jpg')


def gen_text(data):
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 60)
    draw_text.text(
        (100, 20),
        data,
        font = font,
        fill=('#1C0606')
        )
    draw_text.text(
        (100, 434),
        data,
        font = font,
        fill=('#1C0606')
    )
    draw_text.text(
        (100, 217),
        data,
        font=font,
        fill=('#1C0606')
    )
    im.show()

data = 'test text'


gen_text(data)