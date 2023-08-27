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

    @abstractmethod
    def level_up(self):
        pass

    def get_img(self):
        return self.__class__.img


class House(AbstractObj):
    typ = "House"
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'house2.png')), (18, 18)), 0)

    def __init__(self):
        self.need_item = "Tree"
        self.cost = 50
        self.level = 1
        self.health = 100

    def level_up(self):
        self.health += 50
        self.cost += 50


class Resources(ABC):
    img = None

    def __init__(self, healthe=0):
        self.past_time = 0
        self.have_miners = False
        self.healthe = healthe
        self.time = 10
        self.field = None

    def get_img(self):
        return self.__class__.img

    def get_type(self):
        return self.__class__.__name__

    def field_state(self, field):
        self.field = field

    def mining(self, human):
        if time.time_ns() - self.past_time > 100000:
            if self.healthe <= 0:
                self.field.delete_obj()
                human.actualize_field(self.field)
                human.del_current_obj(self)
                self.field = None
            else:
                self.healthe -= 10
                human.dict_inventory[self.get_type()] += 1
                self.past_time = time.time_ns()

            human.skills_up(self.get_type())


    def conf_obj(self, status):
        self.have_miners = status

    def get_pos(self):
        return self.field.get_posX(), self.field.get_posY()


class Gold(Resources):
    def __init__(self):
        super(Gold, self).__init__(1000)

    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'gold.png')), (18, 18)), 0)


class Iron(Resources):
    def __init__(self):
        super(Iron, self).__init__(600)

    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'iron.png')), (18, 18)), 0)


class Copper(Resources):
    def __init__(self):
        super(Copper, self).__init__(450)

    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'copper.png')), (18, 18)), 0)


class Stone(Resources):
    def __init__(self):
        super(Stone, self).__init__(1100)

    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'stone.png')), (18, 18)), 0)


class Tree(Resources):

    def __init__(self):
        super(Tree, self).__init__(695)

    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'Tree.png')), (18, 18)), 0)


class Berries(Resources):
    img = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(os.path.join('image', 'berries.png')), (18, 18)), 0)
