import numpy as np
import requests


def update(id, name, frequency, amplitude=1.0, nodwells=[True, True],
           duration=2, interval=250e-6):
  fconfig = {}

  if isinstance(frequency, list):
    fconfig['mode'] = 'sweep'
    fconfig['value'] = 0
    fconfig['limits'] = frequency
  else:
    fconfig['mode'] = 'const'
    fconfig['value'] = frequency
    fconfig['limits'] = [0, 0]

  aconfig = {}
  if isinstance(amplitude, np.ndarray):
    aconfig['mode'] = 'playback'
    aconfig['data'] = amplitude.tolist()
    aconfig['value'] = 1.0
  else:
    aconfig['mode'] = 'const'
    aconfig['value'] = amplitude
    aconfig['data'] = []

  headers = {'Content-Type': 'application/json'}
  payload = {
      'id': id,
      'name': name,
      'amplitude': {
          'mode': aconfig['mode'],
          'const': {
              'value': aconfig['value'],
          },
          'playback': {
              'trigger': True,
              'duplex': False,
              'interval': interval,
              'data': aconfig['data']
          }
      },
      'phase': {
          'mode': 'const',
          'value': 0
      },
      'frequency': {
          'mode': fconfig['mode'],
          'const': {
              'value': fconfig['value']
          },
          'sweep': {
              'nodwells': nodwells,
              'limits': fconfig['limits'],
              'duration': duration
          }
      }
  }

  response = requests.put(f'http://172.22.22.24:6200/devices/dds/{id}',
                          headers=headers, json=payload)
  response.raise_for_status()

  return response


def vertical(**kargs):
  return update(9, 'Bodo Vertical', **kargs)


def horizontal(**kargs):
  return update(8, 'Bodo horizontal', **kargs)
