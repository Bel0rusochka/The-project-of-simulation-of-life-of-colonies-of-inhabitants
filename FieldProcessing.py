import Human
import Obj
from Field import *
import Resources
from Human import *
import random
import time
from Obj import *


class FieldProcessing:
    lstX_field = []
    count = 0

    @staticmethod
    def gen_resources(count, class_obj):
        while count != 0:
            random.seed(time.time())
            i = random.randint(0, len(FieldProcessing.lstX_field) - 1)
            j = random.randint(0, len(FieldProcessing.lstX_field[0]) - 1)
            if not FieldProcessing.lstX_field[i][j].is_obj():
                FieldProcessing.lstX_field[i][j].add_obj(class_obj())

                count -= 1

    @staticmethod
    def can_moving(human, direction):
        pos = human.get_pos()
        if direction == "R" and (pos[0] + 1 != len(FieldProcessing.lstX_field)):
            return True
        elif direction == "L" and (pos[0] - 1) >= 0:
            return True
        elif direction == "U" and (pos[1] - 1) >= 0:
            return True
        elif direction == "D" and (pos[1] + 1 != len(FieldProcessing.lstX_field[0])):
            return True
        elif direction == "RU" and (pos[0] + 1 != len(FieldProcessing.lstX_field)) and (pos[1] - 1) >= 0:
            return True
        elif direction == "RD" and (pos[0] + 1 != len(FieldProcessing.lstX_field)) and (
                pos[1] + 1 != len(FieldProcessing.lstX_field[0])):
            return True
        elif direction == "LU" and (pos[0] - 1) >= 0 and (pos[1] - 1) >= 0:
            return True
        elif direction == "LD" and (pos[0] - 1) >= 0 and (pos[1] + 1 != len(FieldProcessing.lstX_field[0])):
            return True
        else:
            return False

    @staticmethod
    def moving(human, direction):
        if FieldProcessing.can_moving(human, direction) and FieldProcessing.count == 0:
            pos = human.get_pos()
            human.field.delete_human(human)
            if direction == "R":
                FieldProcessing.lstX_field[pos[0] + 1][pos[1]].add_human(human)
                FieldProcessing.count = 10
            elif direction == "L":
                FieldProcessing.lstX_field[pos[0] - 1][pos[1]].add_human(human)
                FieldProcessing.count = 10
            elif direction == "U":
                FieldProcessing.lstX_field[pos[0]][pos[1] - 1].add_human(human)
                FieldProcessing.count = 10
            elif direction == "D":
                FieldProcessing.lstX_field[pos[0]][pos[1] + 1].add_human(human)
                FieldProcessing.count = 10
            elif direction == "RD":
                FieldProcessing.lstX_field[pos[0] + 1][pos[1] + 1].add_human(human)
                FieldProcessing.count = 10
            elif direction == "RU":
                FieldProcessing.lstX_field[pos[0] + 1][pos[1] - 1].add_human(human)
                FieldProcessing.count = 10
            elif direction == "LD":
                FieldProcessing.lstX_field[pos[0] - 1][pos[1] + 1].add_human(human)
                FieldProcessing.count = 10
            elif direction == "LU":
                FieldProcessing.lstX_field[pos[0] - 1][pos[1] - 1].add_human(human)
                FieldProcessing.count = 10
        else:
            FieldProcessing.count -= 1

    @staticmethod
    def gen_filed():
        for i in range(0, 73):
            lstX_field = []
            for j in range(0, 33):
                lstX_field.append(Field(i, j))
            FieldProcessing.lstX_field.append(lstX_field)

        FieldProcessing.gen_resources(600, Resources.Tree)
        FieldProcessing.gen_resources(400, Resources.Berries)
        # FieldProcessing.gen_resources(100, Resources.Stone)
        # FieldProcessing.gen_resources(50, Resources.Iron)
        # FieldProcessing.gen_resources(45, Resources.Copper)
        # FieldProcessing.gen_resources(20, Resources.Gold)

        return FieldProcessing.lstX_field

    @staticmethod
    def get_filed():
        return FieldProcessing.lstX_field

    @staticmethod
    def clean_class():
        FieldProcessing.lstX_field = []
        FieldProcessing.count = 0
