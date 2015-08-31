__author__ = 'TheJoker'


class VisaBONN(object):
    """initialise the BONN power amplifier"""
    def __init__(self, paaddr, resourcemanager):
        self.rm = resourcemanager
        self.PABONN = self.rm.open_resource(paaddr)
#        self.powerrange = range()

    def PAState(self):
        idn = self.PABONN.query('*IDN?')
        if 'BONN' in idn:
            return True
        else:
            return False

    def PAQuery(self, order):
        return self.PABONN.query(order)

    def PAWrite(self, order):
        self.PABONN.write(order)

    def PARead(self, order):
        self.PABONN.write(order)
        return self.PABONN.read()

    def PAClose(self):
        self.PABONN.close()

    def PABand(self, freq):
        """according the frequency set the band number"""
        freq /= 1000000000
        if freq <= 1:
            bandnum = 1
        elif 1 < freq <= 2:
            bandnum = 2
        elif 2 < freq <= 6:
            bandnum = 3
        elif 6 < freq <= 18:
            bandnum = 4
        else:
            return 'wrong frequency set'
        if bandnum in range(1, 5):
            band = 'SW01_' + str(bandnum)
            self.PAWrite(band)
            self.PAWrite('*IDN?')
            return band
        else:
            return 'error order'

    def PAPowerOut(self, order='OFF'):
        """set the RF ON or OFF, default setting is OFF, if wrong order as input will return 'error order'"""
        if order is 'ON' or 'OFF':
            self.PAWrite('AMP_' + order)
            self.PAWrite('*IDN?')
            return 'SG power status: ' + order
        else:
            return 'error order'


if __name__ == '__main__':
    import visa
    # check
    rm = visa.ResourceManager()
    PAAddr = 'GPIB0::7::INSTR'
    PAtest = VisaBONN(PAAddr, rm)
    PAtest.PABand(2)
    print(PAtest.PAPowerOut('OFF'))
