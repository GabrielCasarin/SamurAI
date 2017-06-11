import os
import pygame
import app.settings as settings

IMAGES_DIR = os.path.join(settings.BASE_DIR, "app", "client", "gui", "images")

IMG_NAMES = [
        "Blue-battleaxe", "Blue-sword", "Red-spear", "Blue-spear", "Red-battleaxe", "Red-sword"
    ]
IMG_NAMES_BUTTONS = [
        "Send", "occupy_down", "occupy_right", "occupy_up", "occupy_left", "move_down", "move_right", "move_up", "move_left", "Hide", "Erase", "Empty", "More", "Occupy", "Move"
    ]
IMG_NAMES_INFO = [
        "Green", "Hidden", "Red", "Blue", "Turno"
    ]
cores = {
    "0": [0, 0, 255],
    "1": [80, 180, 255],
    "2": [80, 255, 255],
    "3": [200, 0, 0],
    "4": [255, 120, 80],
    "5": [255, 0, 80],
    "8": [200, 200, 200],
    "9": [20, 20, 20]
}


class Board:
    def __init__(self, n):
        super(Board, self).__init__()
        delta_x = 20
        delta_y = 20
        self.casas = {
            (i, j): {
                "rect": pygame.Rect(30*i + delta_x, 30*j + delta_y, 30, 30),
                "cor": (255,255,255),
            } for i in range(n) for j in range(n)
        }

    def draw(self, surface):
        for casa in self.casas.values():
            pygame.draw.rect(surface, casa["cor"], casa["rect"])
            pygame.draw.rect(surface, (0,0,0), casa["rect"].copy(), 1)


class OrderList(pygame.sprite.Sprite):

    def __init__(self, images, images_buttons):
        self.order = ['0']
        self.centers = [
            ( 40,500),
            (125,500),
            (175,500),
            (225,500),
            (275,500),
            (325,500)
        ]

        self.imgs_sam = [
            "Blue-spear",
            "Blue-sword",
            "Blue-battleaxe"
        ]

        self.imgs_butt = [
            "Send",
            "occupy_down",
            "occupy_right",
            "occupy_up",
            "occupy_left",
            "move_down",
            "move_right",
            "move_up",
            "move_left",
            "Hide"
        ]
        self.IMAGES = images
        self.IMAGES_BUTTONS = images_buttons

    def __str__(self):
        s = 'Order:'
        for i in range(len(self.order)):
            s += ' {}'.format(self.order[i])
        return s

    def setSamurai(self,num):
        self.order[0] = num #str = '0', '1', ou '2'
        self.draw()

    def appendO(self,newOrder):
        self.order.append(newOrder)
        self.draw()

    def popO(self):
        if len(self.order) > 1:
            self.order.pop()
            self.draw()

    def clear(self):
        self.order = self.order[:1]
        self.draw(False)

    def draw(self, screen, update=True):

        order = self.order
        #limpando
        for i in range(6):
            boxImg = self.IMAGES_BUTTONS['Empty']
            boxRect = boxImg.get_rect(center=self.centers[i])
            screen.blit(boxImg,boxRect)
        #order1:
        xImg = self.IMAGES[self.imgs_sam[int(order[0])]]
        xRect = xImg.get_rect(center=self.centers[0])
        screen.blit(xImg,xRect)

        for i in range(1,5):
            if i < len(order):
                xImg = self.IMAGES_BUTTONS[self.imgs_butt[int(order[i])]]
                xRect = xImg.get_rect(center=self.centers[i])
                screen.blit(xImg,xRect)

        if len(order) == 6:
                xImg = self.IMAGES_BUTTONS[self.imgs_butt[int(order[5])]]
                xRect = xImg.get_rect(center=self.centers[5])
                screen.blit(xImg,xRect)

        elif len(order) > 6:
                xImg = self.IMAGES_BUTTONS["More"]
                xRect = xImg.get_rect(center=self.centers[5])
                screen.blit(xImg,xRect)

        if update:
            #print(self)
            pygame.display.update()
