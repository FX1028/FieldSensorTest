__author__ = 'TheJoker'

import time


class VisaController(object):
    def __init__(self, ctaddr, resourcemanager):
        self.rm = resourcemanager
        self.CT2090 = self.rm.open_resource(ctaddr)
        # set the angle limit
        self.CTWrite('N2;CL 0;WL 360')
        # read the preset angle
        self.angle = self.CTReadAngel()

    def CTQuery(self, order):
        return self.CT2090.query(order)

    def CTWrite(self, order):
        self.CT2090.write(order)

    def CTRead(self, order):
        self.CT2090.write(order)
        return self.CT2090.read()

    def CTClose(self):
        self.CT2090.close()

    def CTReadAngel(self):
        angle = self.CTRead('CP?')
        angle = float(angle[1:5])
        return angle

    def CTRoll(self, angle):
        """turn the table to the set angle, if success return True, if operate time """
        waittime = 1
        rolldone = True
        angleorder = 'SK ' + str(angle)
        self.CTWrite(angleorder)
        while int(self.CTQuery('*OPC?')[0]) < 1:
            time.sleep(0.5)
            if waittime > 40:
                rolldone = False
                break
            waittime += 0.5
        return rolldone


if __name__ == '__main__':
    import visa
    rm = visa.ResourceManager()
    CTAddr = 'GPIB0::10::INSTR'
    CT = VisaController(CTAddr, rm)
    print(CT.CTRoll(180))
    CT.CTClose()
