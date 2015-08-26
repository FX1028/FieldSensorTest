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

    def PABand(self, bandnum):
        if bandnum in range(1, 5):
            band = 'SW01_' + str(bandnum)
            self.PAWrite(band)
            self.PAWrite('*IDN?')
            return band
        else:
            return 'error order'

    def PAPowerOut(self, order):
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
