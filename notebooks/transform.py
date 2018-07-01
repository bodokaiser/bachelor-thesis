import numpy as np

from PIL import Image, ImageDraw, ImageFont


# center frequency
center = 100e6
# frequency range
scale = 20e6


def mask(arr):
  i, j = np.argwhere(arr == arr.min()).transpose()

  i = i / arr.shape[0]
  j = j / arr.shape[1]

  x = -scale * i[::1] + center + scale / 2
  y = scale * j[::1] + center - scale / 2

  return x, y


def text(str):
  font = ImageFont.truetype(font='/Library/Fonts/Verdana.ttf', size=20)
  image = Image.new('1', (100, 30), color=0)
  draw = ImageDraw.Draw(image)
  draw.text((0, 0), str, fill=1, font=font)

  return np.array(image.resize((400, 80), Image.ANTIALIAS))[:, :]
