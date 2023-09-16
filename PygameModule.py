import pygame
import time
import concurrent.futures
from multiprocessing import Process
from Field import *
from Obj import *
from Resources import *
from Human import *
from FieldProcessing import *
from Colony import *
from InitialGame import *


class PygameModule:
    def __init__(self, game, WIDTH=1920, HEIGHT=1080):
        self.game = game
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        pygame.font.init()
        self.lst_field = []
        self.lst_obj = []
        self.lst_human = []
        self.run = True
        self.break_event = False

    def start_game(self):
        colony_lst = self.game.get_colony_lst()

        while self.run:
            self.run = Colony.check_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for colony in colony_lst:
                        colony.save_humans_chromosome()
                    self.run = False
                    self.break_event = True

            self.working_parallel()
            self.sorted_obj_to_lst()
            self.drawing()

            self.lst_obj.clear()
            self.lst_human.clear()

        InitialGame.clean_game()
        pygame.quit()

    def working_parallel(self):
        colony_lst = self.game.get_colony_lst()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(lambda obj: obj.working(), colony_lst)
        executor.shutdown()

    def sorted_obj_to_lst(self):
        for i in self.game.get_field():
            for j in i:
                self.lst_field.append(pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 25, 25))
                if j.is_obj():
                    self.lst_obj.append([pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 18, 18), j.obj])
                if len(j.lst_human) != 0:
                    for human in j.lst_human:
                        self.lst_human.append([pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 18, 18), human])

    def drawing(self):
        self.drawing_obj()
        self.draw_status_bar()

        pygame.display.update()

    def draw_status_bar(self):
        WIN = self.WIN
        HEIGHT = WIN.get_height()

        font = pygame.font.SysFont('comicsans', 30)
        counter_width = 0
        for colony in Colony.lst_colony:
            status_bar_rect = pygame.Rect(30 + counter_width, HEIGHT - 210, 110, 200)
            pygame.draw.rect(WIN, (20, 50, 0), status_bar_rect)
            counter_height = 0
            text = font.render("Colony " + str(Colony.lst_colony.index(colony) + 1), 1, (255, 0, 0))
            WIN.blit(text, (40 + counter_width, HEIGHT - 205))
            for item in colony.dict_inventory_and_pers:
                text = font.render(str(item) + ": " + str(colony.dict_inventory_and_pers[item][0]), 1, (255, 0, 0))
                WIN.blit(text, (40 + counter_width, HEIGHT - 180 + counter_height))
                counter_height += 25
            counter_width += 150

    def drawing_obj(self):
        WIN = self.WIN

        WIN.fill((0, 0, 0))
        for i in self.lst_field:
            pygame.draw.rect(WIN, (145, 255, 0), i)

        for i in self.lst_obj:
            pos, obj = i[0], i[1]
            WIN.blit(obj.get_img(), (pos.x, pos.y))

        for i in self.lst_human:
            pos, human = i[0], i[1]
            WIN.blit(human.get_img(), (pos.x, pos.y))

    def get_status_break_event(self):
        return self.break_event
