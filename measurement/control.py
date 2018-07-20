import numpy as np
import requests
import visa

resource_manager = visa.ResourceManager()


class MSOX6004A:

  def __init__(self, hostname, timeout=5000):
    self.resource = resource_manager.open(f'TCPIP0::{hostname}::inst0::INSTR')
    self.resource.timeout = timeout
    self.resource.clear()

  def holla(self):
    return self.resource.query(':*IDN?')

  def single(self):
    return self.resource.write(':SINGle')

  def save(self, filename):
    return self.resource.write(f':SAVE:WMEMory:STARt "\\usb\\{filename}.h5"')

  def capture(self, channel):
    self.resource.write(':WAVeform:FORMat WORD')
    self.resource.write(':WAVeform:BYTeorder LSBFirst')
    self.resource.write(':WAVeform:UNSigned 0')
    self.resource.write(f':WAVeform:SOURce CHANnel{channel}')

    values = self.resource.query_binary_values(
        ':WAVeform:DATA?', datatype='h', container=np.array, header_fmt='ieee')

    xorg = self.resource.query_ascii_values(':WAVeform:XORigin?')[0]
    xinc = self.resource.query_ascii_values(':WAVeform:XINcrement?')[0]
    yorg = self.resource.query_ascii_values(':WAVeform:YORigin?')[0]
    yinc = self.resource.query_ascii_values(':WAVeform:YINcrement?')[0]
    yref = self.resource.query_ascii_values(':WAVeform:YREference?')[0]

    U = yorg + yinc * (values - yref)
    t = np.arange(xorg, xorg + xinc * len(U), xinc)

    return t, U


def trigger():
  response = requests.get('http://172.22.22.35:6200')
  response.raise_for_status()

  return response


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


def aom():
  return update(2, 'Bodo Intensity', frequency=80e6)


def aod_v(**kargs):
  return update(9, 'Bodo Vertical', **kargs)


def aod_h(**kargs):
  return update(8, 'Bodo horizontal', **kargs)
