from PIL import Image, ImageDraw, ImageFont

im = Image.open('photo/krut.jpg')


def gen_text(data_infected, data_dead, data_recovered,delta_infected, delta_dead, delta_recovered):
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('Times.ttc',120)
    font_delta = ImageFont.truetype('Times.ttc', 60)
    draw_text.text(
        (1000, 310),
        '+' + delta_infected,
        font=font_delta,
        fill=('#E0FFFF')
    )
    draw_text.text(
        (350, 1110),
        '+' + delta_dead,
        font=font_delta,
        fill=('#E0FFFF')
    )
    draw_text.text(
        (1600, 1110),
        '+'+ delta_recovered,
        font=font_delta,
        fill=('#E0FFFF')
    )
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


if __name__ == '__main__':
    data_dead = '1000'
    data_recovered = '14561'
    data_infected = '136241'
    delta_infected = '123456'
    delta_dead = '38239'
    delta_recovered = '8759832741'
    gen_text(data_infected, data_dead, data_recovered, delta_infected, delta_dead, delta_recovered)
