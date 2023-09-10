import os
import pygame
from Human import *
from abc import ABC, abstractmethod


# TODO libpng warning: iCCP: known incorrect sRGB profile
# Traceback (most recent call last):
#   File "/home/andrei/Strategi/main.py", line 88, in <module>
#     game()
#   File "/home/andrei/Strategi/main.py", line 81, in game
#     drawing()
#   File "/home/andrei/Strategi/main.py", line 55, in drawing
#     colony4.working()
#   File "/home/andrei/Strategi/Colony.py", line 105, in working
#     human.brain()
#   File "/home/andrei/Strategi/Human.py", line 231, in brain
#     self.extract_res("Tree")
#   File "/home/andrei/Strategi/Human.py", line 195, in extract_res
#     if not target_field.obj.have_miners:
# AttributeError: 'NoneType' object has no attribute 'have_miners'
#
# Process finished with exit code 1


class AbstractObj(ABC):
    img = None

    def __init__(self, need_item, colony_owner):
        self.need_item = need_item
        self.level = 0
        self.health = 100
        self.colony_owner = colony_owner

    @abstractmethod
    def level_up(self):
        pass

    def get_img(self):
        return self.__class__.img

    def get_type(self):
        return self.__class__.__name__

    def field_state(self, field):
        self.field = field


class House(AbstractObj):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'village_house.png')), (18, 18)), 0)

    def __init__(self, colony_owner):
        super().__init__({"Tree": 50}, colony_owner)

    def level_up(self):
        self.health += 50
        self.need_item["Tree"] += 100

    # def owner_human(self, human):


class Barn(AbstractObj):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'barn.png')), (18, 18)), 0)

    def __init__(self, colony_owner):
        super().__init__({"Tree": 20}, colony_owner)

    def level_up(self):
        self.health += 50
        self.need_item["Tree"] += 150


class Tavern(AbstractObj):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'tavern.png')), (18, 18)), 0)

    def __init__(self, colony_owner):
        super().__init__({"Tree": 80, "Stone": 50}, colony_owner)

    def level_up(self):
        self.health += 50
        self.need_item["Tree"] += 120
        self.need_item["Stone"] += 60


class Farm(AbstractObj):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'farm.png')), (18, 18)), 0)

    def __init__(self, colony_owner):
        super().__init__({"Tree": 15}, colony_owner)

    def level_up(self):
        self.health += 50
        self.need_item["Tree"] += 20
