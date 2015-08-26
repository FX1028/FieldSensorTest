__author__ = 'TheJoker'

from Visa8257D import Visa8257D
from VisaBONN import VisaBONN
from VisaNRP import VisaNRP
from EasyDatabase import EasyDatabase
import visa


class FieldSensor(Visa8257D, VisaBONN, VisaNRP, EasyDatabase):
    def __init__(self, dbname, sgaddr='GPIB0::19::INSTR', paaddr='GPIB0::7::INSTR',
                 nrpaddr='RSNRP::0x0003::102279::INSTR'):
        """initialise the test programme"""
        resourcemanager = visa.ResourceManager()
        Visa8257D.__init__(self, sgaddr, resourcemanager)
        VisaBONN.__init__(self, paaddr, resourcemanager)
        VisaNRP.__init__(self, nrpaddr, resourcemanager)
        EasyDatabase.__init__(self, dbname)

        self.NRPRange = [-67, 23]

    def


if __name__ == '__main__':
    test = FieldSensor('adsfaf')
