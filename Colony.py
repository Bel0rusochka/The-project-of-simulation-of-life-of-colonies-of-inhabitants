from typing import Dict, List, Any

from Human import *
import time
import random

from FieldProcessing import *

class Colony:
    lst_colony = []

    def __init__(self, pole, lst_field):
        self.lst_humans = []
        self.dict_field_types = {"Tree": [], "Empty": [], "Gold": [], "Iron": [], "Copper": [], "Stone": [],
                                 "Berries": []}

        self.level_colony = 0
        self.dict_inventory_and_pers = {"Tree": [0, 0], "Iron": [0, 0], "Gold": [0, 0], "Copper": [0, 0],
                                        "Berries": [0, 0], "Stone": [0, 0]}

        self.dict_spec = {"woodman": [], "miner gold": [], "miner stone": [], "miner iron": [], "miner copper": [],
                          "pick up berries": [], "builder": [], "hunter": [], "warrior": [], "farmer": []}
        random.seed(time.time())
        i = random.randint(0, len(FieldProcessing.lstX_field) - 1)
        j = random.randint(0, len(FieldProcessing.lstX_field[0]) - 1)
        self.spawn = [i, j]
        for i in range(0, 5):
            man = Man(pole, self)
            if self.spawn[0] - 2 < 0:
                begin_rand_posX = 0
            else:
                begin_rand_posX = self.spawn[0] - 2
            if self.spawn[0] + 2 > len(FieldProcessing.lstX_field) - 2:
                end_rand_posX = len(FieldProcessing.lstX_field) - 1
            else:
                end_rand_posX = self.spawn[0] + 2

            if self.spawn[1] - 2 < 0:
                begin_rand_posY = 0
            else:
                begin_rand_posY = self.spawn[1] - 2
            if self.spawn[1] + 2 > len(FieldProcessing.lstX_field[0]) - 2:
                end_rand_posY = len(FieldProcessing.lstX_field[0]) - 1
            else:
                end_rand_posY = self.spawn[1] + 2
            while True:
                random.seed(time.time())
                i = random.randint(begin_rand_posX, end_rand_posX)
                j = random.randint(begin_rand_posY, end_rand_posY)
                if not lst_field[i][j].is_human(man):
                    break

            lst_field[i][j].add_human(man)
            self.lst_humans.append(man)
        for i in range(0, 5):
            woman = Woman(pole, self)
            if self.spawn[0] - 2 < 0:
                begin_rand_posX = 0
            else:
                begin_rand_posX = self.spawn[0] - 2
            if self.spawn[0] + 2 > len(FieldProcessing.lstX_field) - 2:
                end_rand_posX = len(FieldProcessing.lstX_field) - 1
            else:
                end_rand_posX = self.spawn[0] + 2

            if self.spawn[1] - 2 < 0:
                begin_rand_posY = 0
            else:
                begin_rand_posY = self.spawn[1] - 2
            if self.spawn[1] + 2 > len(FieldProcessing.lstX_field[0]) - 2:
                end_rand_posY = len(FieldProcessing.lstX_field[0]) - 1
            else:
                end_rand_posY = self.spawn[1] + 2
            while True:
                random.seed(time.time())
                i = random.randint(begin_rand_posX, end_rand_posX)
                j = random.randint(begin_rand_posY, end_rand_posY)
                if not lst_field[i][j].is_human(woman):
                    break

            lst_field[i][j].add_human(woman)
            self.lst_humans.append(woman)
            Colony.lst_colony.append(self)

    def working(self):
        if self.level_colony == 0:

            if int(0.2 * len(self.lst_humans)) > len(self.dict_spec["woodman"]):
                for human in self.lst_humans:
                    if human.spec_human is None:
                        self.dict_spec["woodman"].append(human)
                        human.spec_human = "woodman"
                        human.add_plan("cut down tree")
            # naiti jahody, rozvedat territorii, brevno, postroit domy, ambar, sklad
        elif self.level_colony == 1:
            pass
            # imeti dohod jedy, breven, nacat dobyvat kamen, zoloto, postroit mastersku, fermu, rynok, prokacat dom do level 2
        elif self.level_colony == 2:
            pass
            # imet dohody jdy, zolota, breven, kamne, nacat dobyvat iron, kazarma, kuzna
        elif self.level_colony == 3:
            pass
            # nacat dobycu copper copper, postrijka melnitsy, pushky
        for human in self.lst_humans:
            human.brain()

    def shearing_field(self, dict_field_human):
        for i in self.dict_field_types:
            merged_list = []
            for item in self.dict_field_types[i] + dict_field_human[i]:
                if item not in merged_list:
                    merged_list.append(item)
            self.dict_field_types[i] = merged_list
        return self.dict_field_types

    def add_item(self, human, typ):
        if human.dict_inventory[typ] != 0:
            human.dict_inventory[typ] -= 1
            self.dict_inventory_and_pers[typ][0] += 1

    # def del_item(self):
