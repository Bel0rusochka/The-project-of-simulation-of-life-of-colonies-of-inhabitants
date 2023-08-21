from Field import *
from Obj import *
import pygame
import multiprocessing
from multiprocessing import Queue
from Human import *
import time
from FieldProcessing import *
from Colony import *

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
pygame.font.init()
FPS = 60
pole = FieldProcessing()
lstXY_field = pole.gen_filed()
lst_field = []
lst_obj = []
lst_human = []

colony1 = Colony(pole, lstXY_field)


# colony2 = Colony(pole, lstXY_field)
# colony3 = Colony(pole, lstXY_field)
# colony4 = Colony(pole, lstXY_field)
def drawing():
    WIN.fill((0, 0, 0))
    for i in lst_field:
        pygame.draw.rect(WIN, (145, 255, 0), i)

    for i in lst_obj:
        obj = i[0]
        if isinstance(i[1], House):
            WIN.blit(House.img, (obj.x, obj.y))
        elif isinstance(i[1], Gold):
            WIN.blit(Gold.img, (obj.x, obj.y))
        elif isinstance(i[1], Tree):
            WIN.blit(Tree.img, (obj.x, obj.y))
        elif isinstance(i[1], Stone):
            WIN.blit(Stone.img, (obj.x, obj.y))
        elif isinstance(i[1], Iron):
            WIN.blit(Iron.img, (obj.x, obj.y))
        elif isinstance(i[1], Copper):
            WIN.blit(Copper.img, (obj.x, obj.y))
        elif isinstance(i[1], Berries):
            WIN.blit(Berries.img, (obj.x, obj.y))

        for i in lst_human:
            obj = i[0]
            if isinstance(i[1], Man):
                WIN.blit(Man.img, (obj.x, obj.y))
            elif isinstance(i[1], Woman):
                WIN.blit(Woman.img, (obj.x, obj.y))

    font = pygame.font.SysFont('comicsans', 30)
    counter = 0
    for item in colony1.dict_inventory_and_pers:
        text = font.render(str(item) + ": " + str(colony1.dict_inventory_and_pers[item][0]), 1, (255, 0, 0))
        WIN.blit(text, (40, HEIGHT - 180 + counter))
        counter += 25
    colony1.working()
    # colony2.working()
    # colony4.working()
    # colony3.working()
    pygame.display.update()


def game():
    run = True
    # button = pygame.
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # elif event.type == pygame.MOUSEMOTION:
            #     print("Позиция мыши: ", event.pos)
            #     # elif event.type == pygame.MOU
            #     # print("Позиция мыши: ", event.pos)

        for i in lstXY_field:
            for j in i:
                lst_field.append(pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 25, 25))
                if j.is_obj():
                    lst_obj.append([pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 18, 18), j.obj])
                if len(j.lst_human) != 0:
                    for human in j.lst_human:
                        lst_human.append([pygame.Rect(0 + 26 * j.get_posX(), +26 * j.get_posY(), 18, 18), human])

        drawing()
        lst_obj.clear()
        lst_human.clear()
    pygame.quit()


if __name__ == "__main__":
    game()
