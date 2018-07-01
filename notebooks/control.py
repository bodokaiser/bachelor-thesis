import numpy as np
import requests


def update(id, name, frequency, nodwells=[True, True], duration=2):
  if isinstance(frequency, np.ndarray):
    mode = 'const'
    value = 100e6
    limits = [0, 0]
    data = frequency.tolist()
  elif isinstance(frequency, list):
    mode = 'sweep'
    limits = frequency
    value = 100e6
    data = []
  else:
    mode = 'playback'
    value = frequency
    limits = [0, 0]
    data = []

  headers = {'Content-Type': 'application/json'}
  payload = {
      'id': id,
      'name': name,
      'amplitude': {'mode': 'const', 'value': 1},
      'phase': {'mode': 'const', 'value': 0},
      'frequency': {
          'mode': mode,
          'const': {'value': value},
          'sweep': {'nodwells': nodwells, 'limits': limits,
                    'duration': duration},
          'playback': {'trigger': False, 'duplex': False,
                       'interval': 1e-5, 'data': data}
      }
  }

  response = requests.put(f'http://beaglebone.local:6200/devices/dds/{id}',
                          headers=headers, json=payload)
  response.raise_for_status()

  return response


def vertical(frequency, **kargs):
  return update(9, 'Bodo Vertical', frequency, **kargs)


def horizontal(frequency, **kargs):
  return update(8, 'Bodo horizontal', frequency, **kargs)
