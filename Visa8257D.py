__author__ = 'TheJoker'


class Visa8257D(object):
    def __init__(self, sgaddr, resourcemanager):
        self.rm = resourcemanager
        self.SG8257 = self.rm.open_resource(sgaddr)
        self.SGWrite('*RST')

    def SGState(self):
        idn = self.SG8257.query('*IDN?')
        if '8257' in idn:
            return True
        else:
            return False

    def SGQuery(self, order):
        return self.SG8257.query(order)

    def SGWrite(self, order):
        self.SG8257.write(order)

    def SGRead(self, order):
        self.SG8257.write(order)
        return self.SG8257.read()

    def SGClose(self):
        self.SG8257.close()

    def SGRef(self, order="INT"):
        """The order command is reference oscillator source: INT (internal) or EXT(external) and return the status"""
        order += '\n'
        self.SGWrite(':ROSCillator:SOURce' + ' ' + order)
        if self.SGQuery(':ROSCillator:SOURce?') == order:
            return 'ref set right'
        else:
            return 'error order'

    def SGCWFrec(self, freq=500000000):
        """Freq is just frequency number, set the frequency and return the frequency number"""
        if freq in range(100000, 31800000000):
            freqcommand = ':FREQ'
            freqwrite = freqcommand + ' ' + str(freq)
            freqquery = freqcommand + '?'
            self.SG8257.write(freqwrite)
            return 'SG frequency: ' + self.SG8257.query(freqquery)
        else:
            return 'Frequency out of range'

    def SGPowerSet(self, power=-135):
        """set the power value of 8257D, the unit is dBm, default power preset with -125dBm"""
        self.SGWrite(':POW' + ' ' + str(power))
        return 'SG Power: ' + self.SGQuery(':POW?')

    def SGPowerOut(self, order='OFF'):
        """set the RF ON or OFF, default setting is OFF, if wrong order as input will return 'error order'"""
        if order is 'ON' or 'OFF':
            self.SGWrite(':OUTP ' + order)
            return 'SG power status: ' + order
        else:
            return 'error order'


if __name__ == '__main__':
    import visa

    rm = visa.ResourceManager()
    SGAddr = 'GPIB0::19::INSTR'
    SG = Visa8257D(SGAddr, rm)
    print(SG.SGQuery('*IDN?'))
    print(SG.SGCWFrec(100000))
    print(SG.SGPowerSet(-20))
    print(SG.SGRef())
    print(SG.SGPowerOut('OFF'))
#    SG.SGClose()
