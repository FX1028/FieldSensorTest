__author__ = 'TheJoker'

from Visa8257D import Visa8257D
from VisaBONN import VisaBONN
from VisaNRP import VisaNRP
from EasyDatabase import EasyDatabase
from Couple import cal_field
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import visa


class FieldSensor(Visa8257D, VisaBONN, VisaNRP, EasyDatabase):
    def __init__(self, dbname, sgaddr='GPIB0::19::INSTR', paaddr='GPIB0::7::INSTR',
                 nrpaddr='RSNRP::0x0003::102279::INSTR'):
        """initialise the test programme"""
        self.app = QApplication(sys.argv)
        resourcemanager = visa.ResourceManager()
#        Visa8257D.__init__(self, sgaddr, resourcemanager)
#        VisaBONN.__init__(self, paaddr, resourcemanager)
        VisaNRP.__init__(self, nrpaddr, resourcemanager)
        EasyDatabase.__init__(self, dbname)

        self.fieldintensityRange = [0, 100]

    def FieldProd(self, freq, fieldintensity):
        """Produce the fieldintensity of specified frequency"""
        sg_output_limit = -5  # unit is dBm set the signal generator output limit
        field = cal_field(freq, fieldintensity)
        # p_meter_disp_dbm, coupler, antenna, e_cal_1w
        powertarget = field[0]
        coupler = field[1]
        antenna = field[2]
        # frequency set
        ms = QMessageBox(QMessageBox.Warning, "提示", "请更换%s耦合器与天线%s进行测试" % (coupler, antenna))
        ms.show()
        self.app.exec_()
        frequency = freq * 1000000000
        print(self.PMSetFreq(frequency))
        self.SGCWFrec(frequency)
        for i in range(0, 6):  # iterate the power output
            if i == 0:
                sg_initial = -30
                self.SGPowerSet(sg_initial)   # set the initial power unit dBm
                self.SGPowerOut('On')
                powercouple = self.PMFetch()
                powerdiff = powertarget - powercouple
                powersg = sg_initial + powerdiff
                if self.SGInRange(powersg) and powersg < sg_output_limit:
                    pass
                else:
                    return 'Error input signal generator power'
                self.SGPowerSet(powersg)
            else:
                powercouple = self.PMFetch()
                powerdiff = powertarget - powercouple
                powersg += powerdiff
                if self.SGInRange(powersg) and powersg < sg_output_limit:
                    pass
                elif
                else:
                    return 'Error input signal generator power'
                self.SGPowerSet(powersg)


        return field


if __name__ == '__main__':
    test = FieldSensor('adsfaf')
    print(test.FieldProd(1.5, 20))
