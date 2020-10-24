from PIL import Image, ImageDraw, ImageFont

im = Image.open('photo/krut.jpg')


def gen_text(data_infected, data_dead, data_recovered):
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 30)
    draw_text.text(
        (315, 30),
        data_infected,
        font=font,
        fill=('#1C0606')
    )
    draw_text.text(
        (140, 120),
        data_dead,
        font=font,
        fill=('#1C0606')
    )
    draw_text.text(
        (520, 120),
        data_recovered,
        font=font,
        fill=('#1C0606')
    )
    im.show()


data_dead = '1000'
data_recovered = '14561'
data_infected = '136241'
gen_text(data_infected, data_dead, data_recovered)
