import os
import pygame
import random
import time
from FieldProcessing import *
from Obj import *


class Human:
    plans = {"eating now": 0, "bring res": 1, "sleep": 1, "eating can wait": 1,
             "war": 2, "mine gold": 2, "mine iron": 2, "mine copper": 2, "mine stone": 2, "cut down tree": 2,
             "can long wait eating": 2, "find res": 2}
    commands_plans = ["stop actual", "cancel all", "cancel last", "cancel first", "cancel", "change actual and first on stack"]

    def __init__(self, pole, colony):
        self.dict_skills = {"miner": 0, "cut down tree": 0, "pick up berries": 0, "build": 0}
        self.colony = colony
        self.is_findObj = False
        self.current_dstX = None
        self.current_dstY = None
        self.actual = None
        self.hunger = 100
        self.spec_human = None
        self.dict_field_types = {"tree": [], "empty": [], "gold": [], "iron": [], "copper": [], "stone": [],
                                 "berries": []}
        self.dict_inventory = {"tree": 0, "iron": 0, "gold": 0, "copper": 0, "berries": 0, "stone": 0}
        # self.dict_armor = {"tree": 0, "iron": 0, "gold": 0, "copper": 0}
        self.pole = pole
        self.health = 100
        self.age = 18
        self.damage = 5
        self.dict_plans = dict()
        self.field = None

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

        # print(self.dict_field_types)

    def get_pos(self):
        return self.field.get_posX(), self.field.get_posY()

    def delete_field(self):
        self.field = None

    def skills_up(self, skill):
        if self.dict_skills[skill] <= 5:
            self.dict_skills[skill] += 0.0025
        print(self.dict_skills)

    def bring_colony_rec(self):
        if self.algoritm_moving(self.colony.spawn[0], self.colony.spawn[1]):
            for name in self.dict_inventory:
                self.colony.dict_inventory_and_pers[name][0] += self.dict_inventory[name]
                self.dict_inventory[name] = 0
            self.finished_plan()
        else:
            self.finished_plan()
            # print(self.dict_plans, self.actual)

    def remember_obj(self, field):
        if field is None:
            field = self.field

        if field.is_obj():
            if isinstance(field.obj, Obj.Tree):
                if field not in self.dict_field_types["tree"]:
                    self.dict_field_types["tree"].append(field)
            elif isinstance(field.obj, Obj.MiningGold):
                if field not in self.dict_field_types["gold"]:
                    self.dict_field_types["gold"].append(field)
            elif isinstance(field.obj, Obj.MiningIron):
                if field not in self.dict_field_types["iron"]:
                    self.dict_field_types["iron"].append(field)
            elif isinstance(field.obj, Obj.MiningCopper):
                if field not in self.dict_field_types["copper"]:
                    self.dict_field_types["copper"].append(field)
            elif isinstance(field.obj, Obj.MiningStone):
                if field not in self.dict_field_types["stone"]:
                    self.dict_field_types["stone"].append(field)
            elif isinstance(field.obj, Obj.MiningStone):
                if field not in self.dict_field_types["berries"]:
                    self.dict_field_types["berries"].append(field)
        else:
            if field not in self.dict_field_types["empty"]:
                self.dict_field_types["empty"].append(field)

    def algoritm_moving(self, targetX, targetY):

        pos = self.get_pos()
        if targetX != pos[0] and targetY != pos[1]:
            distR = pow(pow(targetX - (pos[0] + 1), 2) + pow(targetY - pos[1], 2), 0.5)
            distL = pow(pow(targetX - (pos[0] - 1), 2) + pow(targetY - pos[1], 2), 0.5)
            distU = pow(pow(targetX - pos[0], 2) + pow(targetY - (pos[1] - 1), 2), 0.5)
            distD = pow(pow(targetX - pos[0], 2) + pow(targetY - (pos[1] + 1), 2), 0.5)
            distRU = pow(pow(targetX - (pos[0] + 1), 2) + pow(targetY - (pos[1] - 1), 2), 0.5)
            distRD = pow(pow(targetX - (pos[0] + 1), 2) + pow(targetY - (pos[1] + 1), 2), 0.5)
            distLU = pow(pow(targetX - (pos[0] - 1), 2) + pow(targetY - (pos[1] - 1), 2), 0.5)
            distLD = pow(pow(targetX - (pos[0] - 1), 2) + pow(targetY - (pos[1] + 1), 2), 0.5)

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

        if field in self.dict_field_types["tree"]:
            self.dict_field_types["tree"].remove(field)
        elif field in self.dict_field_types["iron"]:
            self.dict_field_types["iron"].remove(field)
        elif field in self.dict_field_types["copper"]:
            self.dict_field_types["copper"].remove(field)
        elif field in self.dict_field_types["gold"]:
            self.dict_field_types["gold"].remove(field)
        elif field in self.dict_field_types["stone"]:
            self.dict_field_types["stone"].remove(field)
        elif field in self.dict_field_types["empty"]:
            self.dict_field_types["empty"].remove(field)
        elif field in self.dict_field_types["berries"]:
            self.dict_field_types["berries"].remove(field)
        self.remember_obj(field)

    def extract_res(self, types):
        lst_obj = self.dict_field_types[types]
        posX, posY = self.get_pos()
        if len(lst_obj) == 0:
            self.hang_out()
        else:
            if not self.is_findObj:
                min_dst = pow(pow(lst_obj[0].get_posX() - posX, 2) + pow(lst_obj[0].get_posY() - posY, 2), 0.5)
                min_dstX = lst_obj[0].get_posX()
                min_dstY = lst_obj[0].get_posY()
                for target_field in lst_obj:
                    if not target_field.obj.have_miners:
                        if min_dst > pow(pow(target_field.get_posX() - posX, 2) + pow(target_field.get_posY() - posY, 2), 0.5):
                            min_dst = pow(pow(target_field.get_posX() - posX, 2) + pow(target_field.get_posY() - posY, 2), 0.5)
                            min_dstX = target_field.get_posX()
                            min_dstY = target_field.get_posY()
                        self.current_dstX = min_dstX
                        self.current_dstY = min_dstY
                        self.is_findObj = True
                if self.is_findObj:
                    self.hang_out()
                else:
                    self.hang_out()
                    self.is_findObj = False
            else:
                if self.algoritm_moving(self.current_dstX, self.current_dstY) and self.field in self.dict_field_types[types]:
                    self.field.obj.mining(self, types)
                else:
                    self.hang_out()
                    self.is_findObj = False


    def brain(self):
        if self.actual is None:
            self.set_actual()
        else:
            if self.actual == "mine gold":
                self.extract_res("gold")
            elif self.actual == "mine iron":
                self.extract_res("iron")
            elif self.actual == "mine copper":
                self.extract_res("copper")
            elif self.actual == "mine stone":
                self.extract_res("stone")
            elif self.actual == "cut down tree":
                self.extract_res("tree")
            elif self.actual in ["eating now", "eating can wait", "can long wait eating"]:
                self.actual = None
                self.hunger = 100
            elif self.actual == "bring res":
                self.bring_colony_rec()
            else:
                self.hang_out()

        if self.hunger < 0:
            self.field.delete_human()
        elif self.hunger <= 15 and self.actual != "eating now":
            del self.dict_plans["eating can wait"]
            self.del_plan()
            self.add_plan("stop actual")
            self.add_plan("eating now")
        elif self.hunger <= 45 and "eating can wait" not in list(
                self.dict_plans.keys()) and "eating can wait" != self.actual:
            del self.dict_plans["can long wait eating"]
            self.del_plan()
            self.add_plan("eating can wait")
        elif self.hunger <= 75 and "can long wait eating" != self.actual and "eating can wait" not in list(
                self.dict_plans.keys()):
            self.add_plan("can long wait eating")
        #self.hunger -= 0.2
        self.age += 0.0001
        self.dict_field_types = self.colony.shearing_field(self.dict_field_types)

        # self.add_plan("cut down tree")
        if self.actual == "wait":
            self.set_actual()
        # print(self.dict_plans, self.dict_field_types)

    def hang_out(self):
        posX, posY = self.get_pos()
        if (self.current_dstX is None and self.current_dstY is None) or self.algoritm_moving(self.current_dstX,
                                                                                             self.current_dstY):
            if posX - 2 < 0:
                begin_rand_posX = 0
            else:
                begin_rand_posX = posX - 2
            if posX + 2 > len(FieldProcessing.lstX_field) - 2:
                end_rand_posX = len(FieldProcessing.lstX_field) - 1
            else:
                end_rand_posX = posX + 2

            if posY - 2 < 0:
                begin_rand_posY = 0
            else:
                begin_rand_posY = posY - 2
            if posY + 2 > len(FieldProcessing.lstX_field[0]) - 2:
                end_rand_posY = len(FieldProcessing.lstX_field[0]) - 1
            else:
                end_rand_posY = posY + 2

            random.seed(time.time())
            i = random.randint(begin_rand_posX, end_rand_posX)
            j = random.randint(begin_rand_posY, end_rand_posY)
            while True:
                if posX == i and posY == j:
                    i = random.randint(begin_rand_posX, end_rand_posX)
                    j = random.randint(begin_rand_posY, end_rand_posY)
                else:
                    break
            # counter = 0
            # while True:
            #     if counter == 99999999:
            #         break
            #     field = FieldProcessing.lstX_field[i][j]
            #     for typ in self.dict_field_types:
            #         if field in self.dict_field_types[typ] or field == self.field:
            #             i = random.randint(begin_rand_posX, end_rand_posX)
            #             j = random.randint(begin_rand_posY, end_rand_posY)
            #             break
            #     else:
            #         break
            #     counter +=1
            self.current_dstX = i
            self.current_dstY = j


class Man(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'man.png')), (18, 18)), 0)


class Woman(Human):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'woman.png')), (18, 18)), 0)
