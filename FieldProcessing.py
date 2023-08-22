import Human
import Obj
from Field import *

from Human import *
import random
import time
from Obj import *


class FieldProcessing:
    lstX_field = []
    count = 0

    @staticmethod
    def gen_resources(count, typ):
        while count != 0:
            random.seed(time.time())
            i = random.randint(0, len(FieldProcessing.lstX_field) - 1)
            j = random.randint(0, len(FieldProcessing.lstX_field[0]) - 1)
            if not FieldProcessing.lstX_field[i][j].is_obj():
                if typ == "Tree":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Tree())
                elif typ == "Gold":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Gold())
                elif typ == "Iron":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Iron())
                elif typ == "Stone":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Stone())
                elif typ == "Copper":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Copper())
                elif typ == "Berries":
                    FieldProcessing.lstX_field[i][j].add_obj(Obj.Berries())
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
        elif direction == "RD" and (pos[0] + 1 != len(FieldProcessing.lstX_field)) and (pos[1] + 1 != len(FieldProcessing.lstX_field[0])):
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
        for i in range(0, 74):
            lstX_field = []
            for j in range(0, 33):
                lstX_field.append(Field(i, j))
            FieldProcessing.lstX_field.append(lstX_field)

        FieldProcessing.gen_resources(400, "Tree")
        FieldProcessing.gen_resources(200, "Berries")
        FieldProcessing.gen_resources(100, "Stone")
        FieldProcessing.gen_resources(50, "Iron")
        FieldProcessing.gen_resources(45, "Copper")
        FieldProcessing.gen_resources(20, "Gold")

        return FieldProcessing.lstX_field
