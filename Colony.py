from Human import *
import time
import random
from FieldProcessing import *
import neuralnetwork


class Colony:
    lst_colony = []

    def __init__(self, pole, lst_field):
        self.pole = pole
        self.lst_field = lst_field
        self.spawn = None
        self.lst_humans = []
        self.lst_obj = []
        self.dict_field_types = {"Tree": [], "Empty": [], "Gold": [], "Iron": [], "Copper": [], "Stone": [],
                                 "Berries": [], "House":[]}

        self.level_colony = 0
        self.dict_inventory_and_pers = {"Tree": [0, 0], "Iron": [0, 0], "Gold": [0, 0], "Copper": [0, 0],
                                        "Berries": [0, 0], "Stone": [0, 0]}
        self.spawn_human()
        self.net = neuralnetwork.NNetwork(5, 4, 4)
        self.set_chromosome_humans()

    def set_chromosome_humans(self):
        for hm in self.lst_humans:
            net = neuralnetwork.NNetwork(5, 4, 4)
            hm.set_chromosome(net.get_weights())

    def spawn_human(self):
        random.seed(time.time())
        i = random.randint(0, len(FieldProcessing.lstX_field) - 1)
        j = random.randint(0, len(FieldProcessing.lstX_field[0]) - 1)
        self.spawn = (i, j)

        self.spawn_conf(Man)
        self.spawn_conf(Woman)

        Colony.lst_colony.append(self)

    def spawn_conf(self, HumanObj):

        spawn_x, spawn_y = self.spawn
        pole = self.pole
        lst_field = self.lst_field

        for i in range(0, 5):
            human = HumanObj(pole, self)
            if spawn_x - 2 < 0:
                begin_rand_posX = 0
            else:
                begin_rand_posX = spawn_x - 2
            if spawn_x + 2 > len(FieldProcessing.lstX_field) - 2:
                end_rand_posX = len(FieldProcessing.lstX_field) - 1
            else:
                end_rand_posX = spawn_x + 2

            if spawn_x - 2 < 0:
                begin_rand_posY = 0
            else:
                begin_rand_posY = spawn_y - 2
            if spawn_y + 2 > len(FieldProcessing.lstX_field[0]) - 2:
                end_rand_posY = len(FieldProcessing.lstX_field[0]) - 1
            else:
                end_rand_posY = spawn_y + 2
            while True:
                random.seed(time.time())
                i = random.randint(begin_rand_posX, end_rand_posX)
                j = random.randint(begin_rand_posY, end_rand_posY)
                if not lst_field[i][j].is_human(human):
                    break

            lst_field[i][j].add_human(human)
            self.lst_humans.append(human)

    def working(self):
        for human in self.lst_humans:
            self.net.set_weights(human.chromosome)

            lst_action = self.net.predict(
                [human.health, human.hunger, self.level_colony, self.dict_inventory_and_pers["Tree"][0],
                 self.dict_inventory_and_pers["Berries"][0]])
            lst_action = list(map(lambda x: round(x, 5), lst_action))
            human.set_actual(lst_action.index(max(lst_action)))
            human.brain()
            # print(human.chromosome[0:int(len(human.chromosome) / 2)])
            self.crossing_over()
        # print(self.select_chromosomes())
        # print("________________________________")

    def shearing_field(self, dict_field_human):
        for i in self.dict_field_types:
            merged_set = set(self.dict_field_types[i]) | set(dict_field_human[i])
            self.dict_field_types[i] = list(merged_set)
        return self.dict_field_types

    def add_obj_and_level_up(self, obj):
        self.lst_obj.append(obj)
        self.level_colony += 0.025

    def get_items(self, types, count):
        if self.dict_inventory_and_pers[types][0] - count >= 0:
            self.dict_inventory_and_pers[types][0] -= count
            return count
        return 0

    def select_chromosomes(self):
        lst_chromosomes = [hm.chromosome for hm in sorted(self.lst_humans, key=lambda x: x.reword)]
        return lst_chromosomes[0:round(0.4 * len(self.lst_humans))]

    def mutation_humans(self):
        for hm in self.lst_humans:
            hm.mutation_chromosome(0.005)

    def change_chromosome(self, lst_chromosomes):
        for num, hm in enumerate(self.lst_humans):
            hm.set_chromosome(lst_chromosomes[num])

    def crossing_over(self):
        print(len(self.lst_humans))
        populations = self.select_chromosomes()
        new_populations = []
        for num1, chromosome1 in enumerate(populations):
            for num2, chromosome2 in enumerate(populations):
                if num1 < num2:
                    temp1_chromosome = np.concatenate((chromosome1[:len(chromosome1)//2], chromosome2[len(chromosome1)//2:]))
                    new_populations.append(temp1_chromosome)
                    temp2_chromosome = np.concatenate((chromosome2[:len(chromosome1) // 2], chromosome1[len(chromosome1) // 2:]))
                    new_populations.append(temp2_chromosome)
                    temp3_chromosome = np.concatenate((chromosome2[len(chromosome1) // 2:], chromosome1[:len(chromosome1) // 2]))
                    new_populations.append(temp3_chromosome)
                    temp4_chromosome = np.concatenate((chromosome1[len(chromosome1) // 2:], chromosome2[:len(chromosome1) // 2]))
                    new_populations.append(temp4_chromosome)
        new_populations = random.sample(new_populations, len(self.lst_humans))
        self.change_chromosome(new_populations)
        self.mutation_humans()



print(round(0.45 * 6))