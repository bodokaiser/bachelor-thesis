import visa
import numpy as np
import time

from matplotlib import pyplot as plt

rm = visa.ResourceManager()

scope = rm.open_resource('TCPIP0::172.22.22.30::inst0::INSTR')
scope.timeout = 5000
scope.clear()

print(scope.query("*IDN?"))
#Leeren des Triggereventspeichers
print(scope.query('TER?'))

def capture(channel):
    #Versetzen in RUN
    scope.write(':RUN')
    
    triggered = 0
    #Wenn ein Triggerevent auftrat lieftert TER? 1 sonst 0
    while(not(triggered == 1)):
        scope.write('TER?')
        triggered = (int)(scope.read())
        #Nur zu debug Zwecken
        print(triggered)
    
    scope.write(f':DIGitize CHANnel{channel}')
    scope.write(':WAVeform:FORMat WORD')

    #Bitreihenfolge auf LSBFirst
    scope.write(':WAVeform:BYTeorder %s' % ('LSBFirst'))

    #Beim parsen wird das Vorzeichen berücksichtigt, Unsigned false
    scope.write(':WAVeform:UNSigned %d' % (0))
    scope.write(f':WAVeform:SOURce CHANnel{channel}')

    #Header auf IEEE
    values = scope.query_binary_values(':WAVeform:DATA?',
        datatype='h', container=np.array, header_fmt=u'ieee')

    xorg = scope.query_ascii_values(':WAVeform:XORigin?')[0]
    xinc = scope.query_ascii_values(':WAVeform:XINcrement?')[0]
    yorg = scope.query_ascii_values(':WAVeform:YORigin?')[0]
    yinc = scope.query_ascii_values(':WAVeform:YINcrement?')[0]
    yref = scope.query_ascii_values(':WAVeform:YREference?')[0]


    #Werte ergeben sich aus dem Nullwert yref, der Teilung yinc und dem Offset yorg
    U = (values-yref)*yinc+yorg 

    t = np.arange(xorg, xorg + len(U)*xinc, xinc)

    return t, U

# configure the oscilloscope over the front panel to use external,
# rising edge trigger signal in normal mode
#input("configure scope and press enter when ready")

time.sleep(2)

# get values
t, U = capture(1)

# plot result
plt.plot(t, U)
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.show()

