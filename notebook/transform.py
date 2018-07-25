import numpy as np


def fft(t, x):
  T = t[1] - t[0]
  N = len(x)

  P = np.abs(np.fft.fft(x)) / N
  f = np.linspace(0, 1 / T, N)

  return f[:N // 2], P[:N // 2]
