import os
import pygame
from Human import *
from abc import ABC, abstractmethod


class AbstractObj(ABC):
    def level_up(self):
        self.health += 50
        self.cost += 50



class House(AbstractObj):
    def __init__(self):
        self.cost = 50
        self.level = 1
        self.health = 100

    typ = "House"
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'house2.png')), (18, 18)), 0)


class Resources(ABC):
    def __init__(self):
        self.past_time = 0
        self.have_miners = False
        self.cost = 50
        self.healthe = 700
        self.time = 10
        self.field = None

    def get_type(self):
        return self.__class__.__name__
    def field_state(self, field):
        self.field = field

    def mining(self, human, typ):
        if time.time_ns() - self.past_time > 100000:
            if self.healthe == 0:
                self.field.delete_obj()
                human.actualize_field(self.field)
                human.is_findObj = False
                self.field = None
                human.add_plan("bring res")
                human.add_plan("change actual and first on stack")
                self.conf_obj(False)
            else:
                self.conf_obj(True)
                self.healthe -= 10
                human.dict_inventory[typ] += 1
                self.past_time = time.time_ns()

            # TODO make this code better with isinstance
            if typ == "wood":
                human.skills_up("cut down tree")
            elif typ in ["iron", "gold", "copper", "stone"]:
                human.skills_up("miner")
            elif typ == "berries":
                human.skills_up("pick up berries")

    def conf_obj(self, status):
        self.have_miners = status

    def get_pos(self):
        return self.field.get_posX(), self.field.get_posY()


class Gold(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'gold.png')), (18, 18)), 0)


class Iron(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'iron.png')), (18, 18)), 0)


class Copper(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'copper.png')), (18, 18)), 0)


class Stone(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'stone.png')), (18, 18)), 0)


class Tree(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'Tree.png')), (18, 18)), 0)


class Berries(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'berries.png')), (18, 18)), 0)
