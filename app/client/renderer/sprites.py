import pygame
import app.settings as settings


class Board:
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


class Samurai(pygame.sprite.Sprite):
    def __init__(self, num, images, images_buttons, images_info):
        super(Samurai, self).__init__()

        self.num = num
        self.IMAGES = images
        self.IMAGES_BUTTONS = images_buttons
        self.IMAGES_INFO = images_info

        if num == 0:
            self.img_name = "Blue-spear"
            self.image = self.IMAGES[self.img_name]

        elif num == 1:
            self.img_name = "Blue-sword"
            self.image = self.IMAGES[self.img_name]

        elif num == 2:
            self.img_name = "Blue-battleaxe"
            self.image = self.IMAGES[self.img_name]

        elif num == 3:
            self.img_name = "Red-spear"
            self.image = self.IMAGES[self.img_name]

        elif num == 4:
            self.img_name = "Red-sword"
            self.image = self.IMAGES[self.img_name]

        elif num == 5:
            self.img_name = "Red-battleaxe"
            self.image = self.IMAGES[self.img_name]

        else:
            raise Exception("Samurai de número %d não existe" % num)

        self.rect = self.image.get_rect(center=(-100,-100))

        self.x = -1
        self.y = -1
        self.hidden = 0
        self.treatment = 0
        self.order_status = 0

    def _set_center(self, center):
        self.rect = self.image.get_rect(center=center)

    def update(self, surface, board, x, y, order_status, hidden, treatment):
        self.x, self.y, self.order_status, self.hidden, self.treatment = int(x), int(y), int(order_status), int(hidden), int(treatment)
        if (self.x, self.y) != (-1, -1):
            self._set_center(board.casas[(self.x,self.y)]['rect'].center)
            # draw board
            if self.rect.centerx >= 0 and self.rect.centery >= 0:
                surface.blit(self.image, self.rect)

        #Posicao de referencia
        centerStat = (520 + 140*(self.num//3), 320 + (self.num%3)*45)

        #Box
        boxImg = self.IMAGES_BUTTONS['Empty']
        boxRect = boxImg.get_rect(center=centerStat)
        surface.blit(boxImg,boxRect)

        #Weapon
        statusRect = self.image.get_rect(center=centerStat)
        surface.blit(self.image,statusRect)

        #redBar
        redBar = pygame.Rect(centerStat[0] + 25, centerStat[1] + 5, 5*18, 10)
        pygame.draw.rect(surface, (255, 0, 0), redBar)

        #greenBar
        greenBar = pygame.Rect(centerStat[0] + 25,centerStat[1] + 5, 5*(18 - self.treatment), 10)
        pygame.draw.rect(surface, (0, 215, 0), greenBar)

        #blackBord
        pygame.draw.rect(surface, (0, 0, 0), redBar, 1)

        #text
        whiteBg = pygame.Rect(centerStat[0] + 80,centerStat[1] - 19, 30, 20)
        pygame.draw.rect(surface, (255, 255, 255), whiteBg)

        texto = myfont.render('{:>2}'.format(str(self.treatment)), 1, (0,0,0))
        surface.blit(texto, (centerStat[0] + 80, centerStat[1] - 19))

        #status: verde = pode jogar, azul = ja jogou, vermelho = machucado (vermelho tem preferencia em azul)
        if self.treatment > 0:
            infoImg = self.IMAGES_INFO['Red']
        elif self.order_status == 1:
            infoImg = self.IMAGES_INFO['Blue']
        else:
            infoImg = self.IMAGES_INFO['Green']
        infoRect = infoImg.get_rect(center=(centerStat[0] - 11, centerStat[1] + 11))
        surface.blit(infoImg,infoRect)

        #statusHidden:

        if self.hidden == 1:
            hImg = self.IMAGES_INFO['Hidden']
            hRect = hImg.get_rect(center=(centerStat[0] + 11, centerStat[1] - 11))
            surface.blit(hImg,hRect)


class Turno(pygame.sprite.Sprite):
    def __init__(self, images_info):
        super(Turno, self).__init__()
        self.IMAGES_INFO = images_info
        self.turn = 0

        self.center = [550,40]
        self.boxImg = 'Turno'
        self.boxRect = self.IMAGES_INFO[self.boxImg].get_rect(center=self.center)

        self.enable = True
        self.infoCenter = [self.center[0]+31,self.center[1]+10]
        self.enableImg = 'Green'
        self.disableImg = 'Red'
        self.enabRect = self.IMAGES_INFO[self.enableImg].get_rect(center=self.infoCenter)

        self.partida = 0 #inicia com 0, assume o valor 1 durante a primeira partida e o valor 2 durante a segunda

    def setPartida(self, partida):
        self.partida = partida

    def setTurn(self, turno):
        self.turn = turno

    def minhaVez(self, player):
        return not (self.turn%2 + player%2 + self.partida%2)%2

    def final(self):
        return self.turn == settings.MAX_TURN - 1

    def update(self, surface):
        surface.blit(self.IMAGES_INFO[self.boxImg],self.boxRect)

        texto = myfont.render('{:>2}'.format(str(self.turn)), 1, (0,0,0))
        surface.blit(texto, (self.center[0]+20,self.center[1]-15))

        if self.minhaVez():
            surface.blit(self.IMAGES_INFO[self.enableImg],self.enabRect)
        else:
            surface.blit(self.IMAGES_INFO[self.disableImg],self.enabRect)


class Acao(pygame.sprite.Sprite):
    def __init__(self, num, images_buttons):
        super(Acao, self).__init__()
        self.IMAGES_BUTTONS = images_buttons

        cmx = 550   #centerMoveX
        cmy = 200   #centerMoveY

        cox = 670   #centerOcuppyX
        coy = 140   #centerOcuppyY

        dPad = 43  #distancia do center do Pad

        if num == 0:
            self.imgName, self.center = "Send"         , (450,        500      )
        elif num == 1:
            self.imgName, self.center = "occupy_down"  , (cox,        coy+dPad)
        elif num == 2:
            self.imgName, self.center = "occupy_right" , (cox+dPad,  coy      )
        elif num == 3:
            self.imgName, self.center = "occupy_up"    , (cox,        coy-dPad)
        elif num == 4:
            self.imgName, self.center = "occupy_left"  , (cox-dPad,  coy      )
        elif num == 5:
            self.imgName, self.center = "move_down"    , (cmx,        cmy+dPad)
        elif num == 6:
            self.imgName, self.center = "move_right"   , (cmx+dPad,  cmy      )
        elif num == 7:
            self.imgName, self.center = "move_up"      , (cmx,        cmy-dPad)
        elif num == 8:
            self.imgName, self.center = "move_left"    , (cmx-dPad,  cmy      )
        elif num == 9:
            self.imgName, self.center = "Hide"         , (670,        240      )
        elif num == 10:
            self.imgName, self.center = "Erase"        , (400,        500      )

    def update(self, surface):
        self.img = self.IMAGES_BUTTONS[self.imgName]
        self.rect = self.img.get_rect(center=self.center)
        surface.blit(self.img,self.rect)

        #textos:
        occImg = self.IMAGES_BUTTONS['Occupy']
        occRect = occImg.get_rect(center=(cox,coy))
        surface.blit(occImg, occRect)
        movImg = self.IMAGES_BUTTONS['Move']
        movRect = movImg.get_rect(center=(cmx,cmy))
        surface.blit(movImg, movRect)


class ButtonSamurai(pygame.sprite.Sprite):
    def __init__(self, images, images_buttons, images_info):
        super(ButtonSamurai, self).__init__()
        self.IMAGES = images
        self.IMAGES_BUTTONS = images_buttons
        self.IMAGES_INFO = images_info
        
        self.center = [550,100]

        self.boxRect = ''
        self.boxImg = 'Empty'
        self.boxRect = self.IMAGES_BUTTONS[self.boxImg].get_rect(center=self.center)

        self.num = 0
        self.img0 = "Blue-spear"
        self.img1 = "Blue-sword"
        self.img2 = 'Blue-battleaxe'
        self.samRect = self.IMAGES[self.img0].get_rect(center=self.center)

    def update(self, surface, samurai):
        #box
        surface.blit(self.IMAGES_BUTTONS[self.boxImg],self.boxRect)

        #samurai
        if self.num == 0:
            surface.blit(self.IMAGES[self.img0],self.samRect)
        elif self.num == 1:
            surface.blit(self.IMAGES[self.img1],self.samRect)
        elif self.num == 2:
            surface.blit(self.IMAGES[self.img2],self.samRect)

        #info
        infoCenter = [self.center[0]-11,self.center[1]+11]

        if samurai.treatment > 0:
            infoImg = self.IMAGES_INFO['Red']
        elif samurai.order_status == 1:
            infoImg = self.IMAGES_INFO['Blue']
        else:
            infoImg = self.IMAGES_INFO['Green']

        infoRect = infoImg.get_rect(center=[self.center[0]-11,self.center[1]+11])
        surface.blit(infoImg,infoRect)

        if samurai.hidden == 1:
            hImg = self.IMAGES_INFO['Hidden']
            hRect = hImg.get_rect(center=[self.center[0]+11,self.center[1]-11])
            surface.blit(hImg,hRect)
