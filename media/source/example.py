import time
import control

# enable 100 MHz AOM signal
control.aom()

# supply 100 MHz signal at 80% amplitude to AOD H
control.aod_h(amplitude=.8, frequency=100e6)

# supply 80 to 120 MHz chirp at 100% amplitude to AOD V on trigger
control.aod_v(frequency=[80e6, 120e6], duration=20e-3)

# initialize scope connection
scope = control.MSOX6004A('172.22.22.30')

# put scope into SINGLE mode to capture a single measurement
scope.single()

# wait 1 s until scope is ready
time.sleep(1)

# fire the trigger signal to scope and dds
control.trigger()

# wait 2 s until scope is ready
time.sleep(2)

# load the voltage trace from scope
scope.data()
