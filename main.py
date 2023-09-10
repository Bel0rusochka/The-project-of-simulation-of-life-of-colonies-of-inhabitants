from Field import *
from Obj import *
from Resources import *
import pygame
from multiprocessing import Process
from Human import *
import time
from FieldProcessing import *
import concurrent.futures
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
colony2 = Colony(pole, lstXY_field)
colony3 = Colony(pole, lstXY_field)
colony4 = Colony(pole, lstXY_field)



def drawing():
    WIN.fill((0, 0, 0))
    for i in lst_field:
        pygame.draw.rect(WIN, (145, 255, 0), i)
    for i in lst_obj:
        pos, obj = i[0], i[1]
        WIN.blit(obj.get_img(), (pos.x, pos.y))

    for i in lst_human:
        pos, human = i[0], i[1]
        WIN.blit(human.get_img(), (pos.x, pos.y))

    font = pygame.font.SysFont('comicsans', 30)

    counter_width = 0

    for colony in Colony.lst_colony:
        status_bar_rect = pygame.Rect(30 + counter_width, HEIGHT-210, 110, 200)
        pygame.draw.rect(WIN,  (20, 50, 0), status_bar_rect)
        counter_height = 0
        text = font.render("Colony " + str(Colony.lst_colony.index(colony) + 1), 1, (255, 0, 0))
        WIN.blit(text, (40 + counter_width, HEIGHT - 205))
        for item in colony.dict_inventory_and_pers:
            text = font.render(str(item) + ": " + str(colony.dict_inventory_and_pers[item][0]), 1, (255, 0, 0))
            WIN.blit(text, (40 + counter_width, HEIGHT - 180 + counter_height))
            counter_height += 25
        counter_width += 150
    pygame.display.update()



def game():
    run = True
    # button = pygame.

    colony_lst = [colony1, colony2, colony3, colony4]
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(lambda obj: obj.working(), colony_lst)

        drawing()
        lst_obj.clear()
        lst_human.clear()
    pygame.quit()


if __name__ == "__main__":
    game()