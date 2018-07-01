import numpy as np
import requests


def update(id, name, frequency):
  if isinstance(frequency, np.ndarray):
    value = 100e6
    data = frequency.tolist()
  else:
    value = frequency
    data = []

  headers = {'Content-Type': 'application/json'}
  payload = {
      'id': id,
      'name': name,
      'amplitude': {'mode': 'const', 'value': 1},
      'phase': {'mode': 'const', 'value': 0},
      'frequency': {
          'const': {'value': value},
          'playback': {'trigger': False, 'duplex': False,
                       'interval': 1e-5, 'data': data}
      }
  }

  response = requests.put(f'http://beaglebone.local:6200/devices/dds/{id}',
                          headers=headers, json=payload)
  response.raise_for_status()

  return response


def vertical(frequency):
  return update(9, 'Bodo Vertical', frequency)


def horizontal(frequency):
  return update(8, 'Bodo horizontal', frequency)
