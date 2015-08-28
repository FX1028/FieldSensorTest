__author__ = 'TheJoker'

import time
from math import log10


class VisaNRP(object):
    def __init__(self, nrpaddr, resourcemanager):
        self.NRPRange = [-67, 23]
        self.rm = resourcemanager
        self.PM = self.rm.open_resource(nrpaddr)
        self.value = -85
#        self.PAWrite('*RST')

    def PMState(self):
        idn = self.PM.query('*IDN?')
        if 'NRP' in idn:
            return True
        else:
            return False

    def PMQuery(self, order):
        return self.PM.query(order)

    def PMWrite(self, order):
        self.PM.write(order)

    def PMRead(self, order):
        self.PM.write(order)
        return self.PM.read()

    def PMClose(self):
        self.PM.close()

    def PMCal(self):
        """Calibrate and zero the power sensor"""
        zerocommand = 'CALibration:ZERO:AUTO ONCE'
        self.PMWrite(zerocommand)

    def PMSetFreq(self, freq=500000000):
        """Freq is just frequency number, set the frequency and return the frequency number"""
        freqcommand = 'SENSe:FREQuency'
        freqwrite = freqcommand + ' ' + str(freq)
        freqquery = freqcommand + '?'
        self.PMWrite(freqwrite)
        return self.PMQuery(freqquery)

    def PMAVERageRESet(self):
        """Reset the average state"""
        self.PMWrite('SENSe:AVERage:RESet')

    def PMAVERageState(self, state='off'):
        """set the average state and return the state, the state parameter is string 'on' or 'off'"""
        if state == 'on':
            self.PMWrite('SENSe:AVERage:STATe ON')
            return 'Average state on'
        elif state == 'off':
            self.PMWrite('SENSe:AVERage:STATe OFF')
            return 'Average state off'
        else:
            return 'Error: wrong command'

    def PMFetch(self):
        """fetch the power value, return the power with unit of dBm,a timeout should import before fetch value"""
        self.PMWrite('INIT:IMM')
        time.sleep(0.5)
        result = self.PMQuery('FETCH?')
        value = float(result.split(',')[0])
        if value < 1e-12:
            return -150.0  # Clip noise
        else:
            return 10.0 * log10(value) + 30.0


if __name__ == '__main__':
    import visa

    rm = visa.ResourceManager()
    NRPtest = VisaNRP('RSNRP::0x0003::102279::INSTR', rm)

    print(NRPtest.PMQuery('*IDN?'))
#    NRPtest.PACal()
    print(NRPtest.PMSetFreq())
    print(NRPtest.PMFetch())
    print(NRPtest.PMFetch())
    NRPtest.PMClose()
