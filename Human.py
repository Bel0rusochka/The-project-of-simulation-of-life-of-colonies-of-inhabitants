import os
from abc import ABC
import pygame
import random
import time
from FieldProcessing import *
from Obj import *


class Human(ABC):
    img = None

    def __init__(self, pole, colony):
        self.pole = pole
        self.colony = colony
        self.lst_commands = ["cut down tree", "extract berries", "build house", "eating"]
        self.dict_skills = {"Gold, Iron, Stone, Cupper mine": 0, "cut down Tree": 0, "pick up Berries": 0, "build": 0}
        self.dict_field_types = {"Tree": [], "Empty": [], "Gold": [], "Iron": [], "Copper": [], "Stone": [],
                                 "Berries": []}
        self.dict_inventory = {"Tree": 0, "Iron": 0, "Gold": 0, "Copper": 0, "Berries": 0, "Stone": 0}
        self.chromosome = []

        self.hunger = 100
        self.health = 100
        self.reword = 0

        self.is_findObj = False
        self.current_dstX = None
        self.current_dstY = None
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

    def set_actual(self, num):
        self.actual = self.lst_commands[num]

    def delete_field(self):
        self.field = None

    def set_chromosome(self, chromosome):
        self.chromosome = chromosome

    def skills_up(self, skill):
        dict_skills = self.dict_skills
        for key_skill in dict_skills:
            if skill in key_skill:
                if dict_skills[key_skill] <= 5:
                    dict_skills[key_skill] += 0.0025

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
            if self.is_findObj:
                self.obj_is_extract()
            else:
                self.obj_not_extract(lst_obj)

    def obj_not_extract(self, lst_obj):
        sorted_lst = list(filter(lambda field: not field.obj.have_miners, lst_obj))
        if 0 != len(sorted_lst):
            try:
                self.find_obj(sorted_lst[0])
            except AttributeError:
                self.actualize_field(sorted_lst[0])
                self.hang_out()
        else:
            self.hang_out()

    def obj_is_extract(self):
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
        self.bring_colony_res()

    def bring_colony_res(self):
        for name in self.dict_inventory:
            self.colony.dict_inventory_and_pers[name][0] += self.dict_inventory[name]
            self.dict_inventory[name] = 0

    def brain(self):
        if self.hunger == 0:
            self.died()
        else:
            self.hunger -= 0.25
            self.dict_field_types = self.colony.shearing_field(self.dict_field_types)

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
            elif self.actual == "bild house":
                self.build()
            elif self.actual == "extract berries":
                self.extract_res("Berries")
            elif self.actual == "eating":
                if self.colony.get_items("Berries", 1) == 1:
                    self.actual = None
                    self.hunger = 100
            else:
                self.hang_out()

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

    def build(self):
        if not self.field.is_obj():
            if self.colony.get_items("Tree", 50) == 50:
                house = Obj.House(self.colony)
                self.field.add_obj(house)
                self.colony.add_obj_and_level_up(house)
        else:
            self.hang_out()

    def died(self):
        self.colony.lst_humans.remove(self)
        self.field.delete_human(self)


class Man(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'man.png')), (18, 18)), 0)


class Woman(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'woman.png')), (18, 18)), 0)
