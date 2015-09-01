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

    def CTAntennaRoll(self, antenna):
        """180: 02     90: 04       270: 03     360: 01"""
        if antenna == 'ETS3160-0316001':
            angel = self.CTReadAngel()
            if angel >= 180:
                self.CTRoll(360)
            else:
                self.CTRoll(0)
        elif antenna == 'ETS3160-0316002':
            self.CTRoll(180)
        elif antenna == 'ETS3160-0316003':
            self.CTRoll(270)
        else:
            self.CTRoll(90)

    def CTAntennaChange(self, antenna):
        """90: 02     0: 04       180: 03     270: 01"""
        if antenna == 'ETS3160-0316003':
            angel = self.CTReadAngel()
            if angel >= 180:
                self.CTRoll(360)
            else:
                self.CTRoll(0)
        elif antenna == 'ETS3160-0316004':
            self.CTRoll(180)
        elif antenna == 'ETS3160-0316001':
            self.CTRoll(90)
        else:
            self.CTRoll(270)

if __name__ == '__main__':
    import visa
    rm = visa.ResourceManager()
    CTAddr = 'GPIB0::10::INSTR'
    CT = VisaController(CTAddr, rm)
    print(CT.CTRoll(180))
    CT.CTClose()
