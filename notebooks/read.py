import numpy as np

from PIL import Image


def image(filename):
  return np.array(Image.open(filename))[:, :, 0]
