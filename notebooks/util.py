import numpy as np


def closeto(x, x0, eps=.01):
  return (x > x0 - eps) & (x < x0 + eps)


def peaktopeak(x):
  return x.max() - x.min()


def argoffset(t, t0, t1):
  i = np.round(np.argwhere(closeto(t, t0)).mean())
  j = np.round(np.argwhere(closeto(t, t1)).mean())

  return int(i), int(j)


def scatter(df, step=100, fstart=90e6, fstop=110e6):
  hdata = []
  vdata = []

  for _, row in df.iterrows():
    d = row['voltage'][::step]
    fstep = (fstop - fstart) / len(d)

    if row['mode'] == 'horizontal':
      fv = row['frequency']

      for i in range(len(d)):
        fh = fstart + fstep * i

        hdata.append((fh, fv, d[i]))

    if row['mode'] == 'vertical':
      fh = row['frequency']

      for i in range(len(d)):
        fv = fstart + fstep * i

        vdata.append((fh, fv, d[i]))

  return np.array(hdata).transpose(), np.array(vdata).transpose()
