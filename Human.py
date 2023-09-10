import os
from abc import ABC
import pygame
import random
import time
from FieldProcessing import *
from Obj import *


class Human(ABC):
    img = None
    plans = {"eating": 0, "bring res": 1, "sleep": 1,
             "war": 2, "mine gold": 2, "mine iron": 2, "mine copper": 2, "mine stone": 2, "cut down tree": 2,
             "can long wait eating": 2, "find res": 2}

    commands_plans = ["stop actual", "cancel all", "cancel last", "cancel first", "cancel",
                      "change actual and first on stack"]

    def __init__(self, pole, colony):
        self.pole = pole
        self.colony = colony

        self.dict_skills = {"Gold, Iron, Stone, Cupper mine": 0, "cut down Tree": 0, "pick up Berries": 0, "build": 0}
        self.dict_field_types = {"Tree": [], "Empty": [], "Gold": [], "Iron": [], "Copper": [], "Stone": [],
                                 "Berries": []}
        self.dict_inventory = {"Tree": 0, "Iron": 0, "Gold": 0, "Copper": 0, "Berries": 0, "Stone": 0}
        self.dict_plans = dict()
        self.chromosome = []  # TODO gen first random chromosome

        self.hunger = 100
        self.sleepy = 0
        self.health = 100
        # self.age = 18
        self.damage = 5

        self.is_findObj = False
        self.current_dstX = None
        self.current_dstY = None
        self.spec_human = None
        self.actual = None
        self.field = None

    def get_img(self):
        return self.__class__.img

    def field_state(self, field):
        self.field = field
        self.remember_obj(field)
        posX, posY = self.get_pos()
        if posX - 1 >= 0:
            self.remember_obj(FieldProcessing.lstX_field[posX - 1][posY])

        if posX + 1 <= len(FieldProcessing.lstX_field) - 1:
            self.remember_obj(FieldProcessing.lstX_field[posX + 1][posY])

        if posY - 1 >= 0:
            self.remember_obj(FieldProcessing.lstX_field[posX][posY - 1])

        if posY + 1 <= len(FieldProcessing.lstX_field[0]) - 1:
            self.remember_obj(FieldProcessing.lstX_field[posX][posY + 1])

    def get_pos(self):
        return self.field.get_posX(), self.field.get_posY()

    def delete_field(self):
        self.field = None

    def skills_up(self, skill):
        dict_skills = self.dict_skills
        for key_skill in dict_skills:
            if skill in key_skill:
                if dict_skills[key_skill] <= 5:
                    dict_skills[key_skill] += 0.0025

    def bring_colony_res(self):
        if self.algoritm_moving(self.colony.spawn[0], self.colony.spawn[1]):
            for name in self.dict_inventory:
                self.colony.dict_inventory_and_pers[name][0] += self.dict_inventory[name]
                self.dict_inventory[name] = 0
            self.finished_plan()

    def remember_obj(self, field):
        if field.is_obj():
            name_obj = field.obj.get_type()
            if field not in self.dict_field_types[name_obj]:
                self.dict_field_types[name_obj].append(field)
        else:
            if field not in self.dict_field_types["Empty"]:
                self.dict_field_types["Empty"].append(field)

    def algoritm_moving(self, targetX, targetY):
        posX, poxY = self.get_pos()
        if targetX != posX or targetY != poxY:
            distR = pow(pow(targetX - (posX + 1), 2) + pow(targetY - poxY, 2), 0.5)
            distL = pow(pow(targetX - (posX - 1), 2) + pow(targetY - poxY, 2), 0.5)
            distU = pow(pow(targetX - posX, 2) + pow(targetY - (poxY - 1), 2), 0.5)
            distD = pow(pow(targetX - posX, 2) + pow(targetY - (poxY + 1), 2), 0.5)
            distRU = pow(pow(targetX - (posX + 1), 2) + pow(targetY - (poxY - 1), 2), 0.5)
            distRD = pow(pow(targetX - (posX + 1), 2) + pow(targetY - (poxY + 1), 2), 0.5)
            distLU = pow(pow(targetX - (posX - 1), 2) + pow(targetY - (poxY - 1), 2), 0.5)
            distLD = pow(pow(targetX - (posX - 1), 2) + pow(targetY - (poxY + 1), 2), 0.5)

            min_dist = min(distR, distL, distU, distD, distRU, distRD, distLU, distLD)
            if min_dist == distU:
                self.pole.moving(self, "U")
            elif min_dist == distD:
                self.pole.moving(self, "D")
            elif min_dist == distRU:
                self.pole.moving(self, "RU")
            elif min_dist == distRD:
                self.pole.moving(self, "RD")
            elif min_dist == distLU:
                self.pole.moving(self, "LU")
            elif min_dist == distLD:
                self.pole.moving(self, "LD")
            elif min_dist == distR:
                self.pole.moving(self, "R")
            elif min_dist == distL:
                self.pole.moving(self, "L")
            return False
        else:
            return True

    def add_plan(self, plan, most_imp=False):
        if most_imp:
            self.dict_plans[plan] = 1
        else:
            if plan in Human.commands_plans:
                if plan == "stop actual":
                    if self.actual is not None:
                        self.add_plan(self.actual, True)
                        self.actual = None
                elif plan == "cancel all":
                    self.dict_plans = dict()
                elif plan == "cancel first":
                    del self.dict_plans[list(self.dict_plans.keys())[0]]
                elif plan == "cancel last":
                    del self.dict_plans[list(self.dict_plans.keys())[-1]]
                elif plan == "cancel":
                    self.actual = None
                elif plan == "change actual and first on stack":
                    if self.actual is not None:
                        tmp = self.actual
                        self.set_actual()
                        self.add_plan(tmp, True)
            else:
                priority = Human.plans[plan]
                if plan not in self.dict_plans.keys():
                    while True:
                        if priority in self.dict_plans.values():
                            priority += 1
                        else:
                            self.dict_plans[plan] = priority
                            break

        self.dict_plans = dict(sorted(self.dict_plans.items(), key=lambda x: x[1]))

    def del_plan(self):
        count = 2
        for i in self.dict_plans:
            if self.dict_plans[i] > 1:
                self.dict_plans[i] = count
                count += 1

    def set_actual(self):
        if len(self.dict_plans.keys()) != 0:
            self.actual = list(self.dict_plans.keys())[0]
            self.dict_plans.pop(self.actual)
            self.del_plan()
        else:
            self.actual = "wait"

    def finished_plan(self):
        self.actual = None
        self.set_actual()

    def actualize_field(self, field):
        for keys in self.dict_field_types:
            if field in self.dict_field_types[keys]:
                self.dict_field_types[keys].remove(field)
                break
        self.remember_obj(field)

    def extract_res(self, types):
        lst_obj = self.dict_field_types[types]
        if len(lst_obj) == 0:
            self.hang_out()
        else:
            if not self.is_findObj:
                self.obj_isnt_find(lst_obj)
            else:
                self.obj_is_find()

    def obj_isnt_find(self, lst_obj):
        sorted_lst = list(filter(lambda field: not field.obj.have_miners, lst_obj))
        if 0 != len(sorted_lst):
            try:
                self.find_obj(sorted_lst[0])
            except AttributeError:
                self.actualize_field(sorted_lst[0])
                self.hang_out()
        else:
            self.hang_out()

    def obj_is_find(self):
        if self.algoritm_moving(self.current_dstX, self.current_dstY):
            try:
                self.field.obj.mining(self)
            except AttributeError:
                self.actualize_field(self.field)
                self.current_dstX = None
                self.current_dstY = None
                self.is_findObj = False

    def find_obj(self, field):
        self.current_dstX = field.get_posX()
        self.current_dstY = field.get_posY()
        self.is_findObj = True
        field.obj.conf_obj(True)

    def del_current_obj(self, obj):
        self.current_dstX = None
        self.current_dstY = None
        self.is_findObj = False
        obj.conf_obj(False)
        self.add_plan("bring res")
        self.add_plan("change actual and first on stack")

    def brain(self):
        if self.actual is None:
            self.set_actual()
        else:
            if self.actual == "mine gold":
                self.extract_res("Gold")
            elif self.actual == "mine iron":
                self.extract_res("Iron")
            elif self.actual == "mine copper":
                self.extract_res("Copper")
            elif self.actual == "mine stone":
                self.extract_res("Stone")
            elif self.actual == "cut down tree":
                self.extract_res("Tree")
            elif self.actual == "bring res":
                self.bring_colony_res()
            else:
                self.hang_out()

        if self.actual in ["eating now", "eating can wait", "can long wait eating"]:
            if self.colony.get_items("Berries", 1) == 1:
                self.actual = None
                self.hunger = 100

        if self.hunger == 0:
            self.field.delete_human()
            self.__del__()

        print( self.hunger)
        self.hunger -= 1
        self.dict_field_types = self.colony.shearing_field(self.dict_field_types)

    def hang_out(self):
        posX, posY = self.get_pos()
        while True:
            try:
                random.seed(time.time())
                i = random.randint(posX - 2, posX + 2)
                j = random.randint(posY - 2, posY + 2)
                if abs(i) == posX and abs(j) == posY:
                    continue
                else:
                    self.pole.get_filed()[abs(i)][abs(j)]
                    self.algoritm_moving(abs(i), abs(j))
                    break
            except IndexError:
                continue


class Man(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'man.png')), (18, 18)), 0)


class Woman(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'woman.png')), (18, 18)), 0)
