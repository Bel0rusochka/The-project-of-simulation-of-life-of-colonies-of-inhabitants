import time


class Field:

    def __init__(self, posX, posY):
        self.lst_human = []
        self.obj = None
        self.posX = posX
        self.posY = posY

    def add_obj(self, obj):
        self.obj = obj
        obj.field_state(self)

    def add_human(self, human):
        self.lst_human.append(human)
        human.field_state(self)

    def get_posX(self):
        return self.posX

    def get_posY(self):
        return self.posY

    def get_obj(self):
        print(self.obj)

    def is_human(self, human):
        return True if human in self.lst_human else False

    def delete_human(self, human):
        human.delete_field()
        self.lst_human.remove(human)

    def delete_obj(self):
        self.obj = None

    def is_obj(self):
        return True if self.obj is not None else False
