import os
import h5py as h5
import numpy as np
import pandas as pd

from PIL import Image


def csv(filename):
  df = pd.read_csv(filename, skiprows=3, header=None, names=[
                   'frequency', 'amplification', 'empty'])
  df = df.drop(columns='empty')
  return df


def image(filename):
  return np.array(Image.open(filename))[:, :, 0]


def timeseries(path):
  data = []

  filenames = [f for f in os.listdir(path) if f.endswith('.h5')]
  filenames.sort()

  for filename in filenames:
    basename = filename.split('.')[0]

    _, U = h5dataset(os.path.join(path, filename), 1)

    data.append({'datetime': basename, 'voltage': U.mean()})

  return pd.DataFrame(data)


def h5dataset(filename, channel):
  with h5.File(filename, 'r') as f:
    dataset = f['Waveforms'][f'Channel {channel}']

    x0 = dataset.attrs['XOrg']
    dx = dataset.attrs['XInc']

    # produces unreasonable voltages i.e. 10e-5 V
    y0 = 0  # dataset.attrs['YOrg']
    dy = 1  # dataset.attrs['YInc']

    y = y0 + dy * dataset[f'Channel {channel} Data'][:]
    x = np.arange(x0, x0 + dx * len(y), dx)

    return x, y


def voltages(path):
  data = []

  for filename in os.listdir(path):
    if not filename.endswith('.h5'):
      continue

    base = filename.split('.')[0].split('-')

    if (len(base) == 3):
      ch = int(base[0][-1])
    else:
      ch = 1

    if base[-2] == 'vsweep':
      mode = 'vertical'
    else:
      mode = 'horizontal'

    freq = base[-1]

    t, U = h5dataset(os.path.join(path, filename), ch)

    data.append({'frequency': int(freq), 'mode': mode, 'channel': ch,
                 'voltage': U, 'time': t})

  return pd.DataFrame(data)
