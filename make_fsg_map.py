from PIL import Image, ImageDraw
from opensimplex import OpenSimplex

WIDTH = 800
HEIGHT = 600
FEATURE_SIZE = 100
CITY_CENTER_WIDTH = WIDTH // 2
CITY_CENTER_HEIGHT = HEIGHT // 2

image_array = []
tmp = OpenSimplex()
im = Image.new("L", (WIDTH, HEIGHT))


def noise_px(width, height, feature_size):
    for y in range(0, height):
        for x in range(0, width):
            value = tmp.noise2d(x / feature_size, y / feature_size)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)


def make_road(city_center_width, city_center_height, width, height):
    on_map = True
    draw = ImageDraw.Draw(im)
    current_spot_x = city_center_width
    current_spot_y = city_center_height

    px = im.load()
    print(px[5, 5])

    while on_map:
        if current_spot_x < width:
            print(px[current_spot_x, current_spot_y])
            draw.point((current_spot_x, current_spot_y), fill=0)
            current_spot_x += 1
        else:
            on_map = False


def write_image(image):
    out = open("web/cities/image.png", "wb")
    image.save(out)
    out.close()


noise_px(WIDTH, HEIGHT, FEATURE_SIZE)
make_road(CITY_CENTER_WIDTH, CITY_CENTER_HEIGHT, WIDTH, HEIGHT)
write_image(im)
