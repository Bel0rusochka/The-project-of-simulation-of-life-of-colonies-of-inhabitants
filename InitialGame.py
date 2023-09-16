from FieldProcessing import *
from Colony import *


class InitialGame:
    def __init__(self):
        self.pole = FieldProcessing()
        self.lstXY_field = self.pole.gen_filed()
        self.colony_lst = []
        self.gen_colony()

    @staticmethod
    def clean_game():
        FieldProcessing.clean_class()
        Colony.clean_class()

    def gen_colony(self, count=4):
        for i in range(count):
            colony = Colony(self.pole, self.lstXY_field)
            self.colony_lst.append(colony)

        Colony.load_humans_chromosome()

    def get_colony_lst(self):
        return self.colony_lst

    def get_pole(self):
        return self.pole

    def get_field(self):
        return self.lstXY_field
