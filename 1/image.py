from PIL import Image, ImageDraw, ImageFont

im = Image.open('photo/krut.jpg')


def gen_text(data_infected, data_dead, data_recovered):
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('Times.ttc',120)
    draw_text.text(
        (1000, 200),
        data_infected,
        font=font,
        fill=('#B22222')
    )
    draw_text.text(
        (350, 1000),
        data_dead,
        font=font,
        fill=('#FF0000')
    )
    draw_text.text(
        (1600, 1000),
        data_recovered,
        font=font,
        fill=('#32CD32')
    )
    im.show()


data_dead = '1000'
data_recovered = '14561'
data_infected = '136241'
gen_text(data_infected, data_dead, data_recovered)
