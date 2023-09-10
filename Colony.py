from Human import *
import time
import random
from FieldProcessing import *


class Colony:
    lst_colony = []

    def __init__(self, pole, lst_field):
        self.pole = pole
        self.lst_field = lst_field
        self.spawn = None
        self.lst_humans = []
        self.lst_obj = []
        self.dict_field_types = {"Tree": [], "Empty": [], "Gold": [], "Iron": [], "Copper": [], "Stone": [],
                                 "Berries": []}

        self.level_colony = 0
        self.dict_inventory_and_pers = {"Tree": [0, 0], "Iron": [0, 0], "Gold": [0, 0], "Copper": [0, 0],
                                        "Berries": [0, 0], "Stone": [0, 0]}

        self.dict_spec = {"woodman": [], "miner gold": [], "miner stone": [], "miner iron": [], "miner copper": [],
                          "pick up berries": [], "builder": [], "hunter": [], "warrior": [], "farmer": []}
        self.spawn_human()

    def spawn_human(self):
        random.seed(time.time())
        i = random.randint(0, len(FieldProcessing.lstX_field) - 1)
        j = random.randint(0, len(FieldProcessing.lstX_field[0]) - 1)
        self.spawn = (i, j)

        self.spawn_conf(Man)
        self.spawn_conf(Woman)

        Colony.lst_colony.append(self)

    def spawn_conf(self, HumanObj):

        spawn_x, spawn_y = self.spawn
        pole = self.pole
        lst_field = self.lst_field

        for i in range(0, 5):
            human = HumanObj(pole, self)
            if spawn_x - 2 < 0:
                begin_rand_posX = 0
            else:
                begin_rand_posX = spawn_x - 2
            if spawn_x + 2 > len(FieldProcessing.lstX_field) - 2:
                end_rand_posX = len(FieldProcessing.lstX_field) - 1
            else:
                end_rand_posX = spawn_x + 2

            if spawn_x - 2 < 0:
                begin_rand_posY = 0
            else:
                begin_rand_posY = spawn_y - 2
            if spawn_y + 2 > len(FieldProcessing.lstX_field[0]) - 2:
                end_rand_posY = len(FieldProcessing.lstX_field[0]) - 1
            else:
                end_rand_posY = spawn_y + 2
            while True:
                random.seed(time.time())
                i = random.randint(begin_rand_posX, end_rand_posX)
                j = random.randint(begin_rand_posY, end_rand_posY)
                if not lst_field[i][j].is_human(human):
                    break

            lst_field[i][j].add_human(human)
            self.lst_humans.append(human)

    def working(self):
        for human in self.lst_humans:
            human.brain()

    def shearing_field(self, dict_field_human):
        for i in self.dict_field_types:
            merged_set = set(self.dict_field_types[i]) | set(dict_field_human[i])
            self.dict_field_types[i] = list(merged_set)
        return self.dict_field_types

    # def add_item(self, human, typ):
    #     if human.dict_inventory[typ] != 0:
    #         human.dict_inventory[typ] -= 1
    #         self.dict_inventory_and_pers[typ][0] += 1

    def add_obj_and_level_up(self, obj):
        self.lst_obj.append(obj)
        self.level_colony += 0.025

    def get_items(self, types, count):
        if self.dict_inventory_and_pers[types][0] - count >= 0:
            self.dict_inventory_and_pers[types][0] -= count
            return count
        return 0

    # def del_item(self):
