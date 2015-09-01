__author__ = 'TheJoker'

from Visa8257D import Visa8257D
from VisaBONN import VisaBONN
from VisaNRP import VisaNRP
from VisaController import VisaController
from EasyDatabase import EasyDatabase
from Couple import cal_field
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import visa


class FieldSensor(Visa8257D, VisaBONN, VisaNRP, VisaController, EasyDatabase):
    def __init__(self, dbname, sgaddr='GPIB0::19::INSTR', paaddr='GPIB0::7::INSTR',
                 nrpaddr='RSNRP::0x0003::102279::INSTR', ctaddr='GPIB0::10::INSTR'):
        """initialise the test programme"""
        resourcemanager = visa.ResourceManager()
        Visa8257D.__init__(self, sgaddr, resourcemanager)
        VisaBONN.__init__(self, paaddr, resourcemanager)
        VisaNRP.__init__(self, nrpaddr, resourcemanager)
        VisaController.__init__(self, ctaddr, resourcemanager)
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
        app = QApplication(sys.argv)
        ms = QMessageBox(QMessageBox.Warning, "提示", "请更换%s耦合器进行测试" % coupler)
        ms.show()
        app.exec_()
        ms = QMessageBox(QMessageBox.Warning, "提示", "请连接%s天线进行测试" % antenna)
        ms.show()
        app.exec_()
        self.CTAntennaChange(antenna)
        ms = QMessageBox(QMessageBox.Warning, "提示", "请确定天线更换完毕并且射频线连接正确")
        ms.show()
        app.exec_()
        self.CTAntennaRoll(antenna)
        sg_initial = -30
        self.SGPowerSet(sg_initial)   # set the initial power unit dBm

        # frequency set
        frequency = freq * 1000000000
        print(self.SGCWFrec(frequency))
        print(self.PMSetFreq(frequency))
        print(self.PABand(frequency))
        self.SGPowerOut('On')
        self.PAPowerOut('ON')

        for i in range(0, 6):  # iterate the power output
            if i == 0:

                powercouple = self.PMFetch()
                print(powercouple)
                powerdiff = powertarget - powercouple
                powersg = sg_initial + powerdiff
                if self.SGInRange(powersg) and powersg < sg_output_limit:
                    self.SGPowerSet(powersg)
                else:
                    ms = QMessageBox(QMessageBox.Warning, 'Alert', "Error input signal generator power")
                    ms.show()
                    app.exec_()
                    break
            else:
                powercouple = self.PMFetch()
                powerdiff = powertarget - powercouple
                powersg += powerdiff
                if self.SGInRange(powersg) and powersg < sg_output_limit:
                    self.SGPowerSet(powersg)
                elif 3 > powerdiff > 1:
                    ms = QMessageBox(QMessageBox.Warning, "提示", "功放到达1dB压缩点")
                    ms.show()
                    app.exec_()
                    break
                else:
                    ms = QMessageBox(QMessageBox.Warning, 'Alert', "Error input signal generator power")
                    ms.show()
                    app.exec_()
        self.PAPowerOut('OFF')
        self.SGPowerOut('OFF')
        print(powercouple)
        return field


if __name__ == '__main__':
    test = FieldSensor('adsfaf')
    print(test.FieldProd(1, 10))
