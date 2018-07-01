import os
import h5py as h5
import numpy as np
import pandas as pd

from PIL import Image


def image(filename):
  return np.array(Image.open(filename))[:, :, 0]


def timeseries(path):
  data = []

  filenames = [f for f in os.listdir(path) if f.endswith('.h5')]
  filenames.sort()

  for filename in filenames:
    basename = filename.split('.')[0]

    with h5.File(os.path.join(path, filename), 'r') as file:
      data.append({
          'datetime': basename,
          'voltage': file['Waveforms']['Channel 1']['Channel 1 Data'][:].mean()
      })

  return pd.DataFrame(data)
