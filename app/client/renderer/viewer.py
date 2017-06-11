import os
import pygame
import app.settings as settings
from .sprites import *
__all__ = ['Viewer']


#image's path
IMAGES_DIR = os.path.join(settings.BASE_DIR, "app", "client", "renderer", "images")
IMG_NAMES = ["Blue-battleaxe", "Blue-sword", "Red-spear", "Blue-spear", "Red-battleaxe", "Red-sword"]
IMG_NAMES_BUTTONS = ["Send", "occupy_down", "occupy_right", "occupy_up", "occupy_left", "move_down", "move_right", "move_up", "move_left", "Hide", "Erase", "Empty", "More", "Occupy", "Move"]
IMG_NAMES_INFO = ["Green", "Hidden", "Red", "Blue", "Turno"]


class Viewer:
    __instance = None
    def __new__(cls):
        if not Viewer.__instance:
            Viewer.__instance = super().__new__(cls)
            pygame.init()
            #definindo a surface
            Viewer.__instance.__screen = pygame.display.set_mode((800,600))
            Viewer.__instance.myfont = pygame.font.SysFont("arial", 15)
            #carrega as imagens
            try:
                IMAGES = {
                    name: pygame.image.load(os.path.join(IMAGES_DIR, "SamurAI-Images", "{}.png".format(name))).convert_alpha()
                    for name in IMG_NAMES
                }

                IMAGES_BUTTONS = {
                    name: pygame.image.load(os.path.join(IMAGES_DIR, "buttons-Images", "{}.png".format(name))).convert_alpha()
                    for name in IMG_NAMES_BUTTONS
                }

                IMAGES_INFO = {
                    name: pygame.image.load(os.path.join(IMAGES_DIR, "info-Images", "{}.png".format(name))).convert_alpha()
                    for name in IMG_NAMES_INFO
                }                
            except Exception as e:
                pygame.quit()
                raise e
            #carrega o icone
            try:
                pygame.display.set_icon(pygame.image.load(os.path.join(IMAGES_DIR, "Icon.png")))
            except Exception as e:
                print(e)
            pygame.display.set_caption('Samurai3x3')
            if settings.SPLASH_SCREEN:
                try:
                    bg = pygame.image.load(os.path.join(IMAGES_DIR, "background.png"))
                except Exception as e:
                    pygame.quit()
                    raise e
                else:
                    Viewer.__instance.__screen.blit(bg, bg.get_rect())
                    pygame.display.update()
                    pygame.time.delay(2000)

            Viewer.__instance.__screen.fill([220,220,220])
            pygame.display.update()

        #definindo o tabuleiro
        Viewer.__instance.__board = Board(settings.size)
        Viewer.__instance.__board.update(Viewer.__instance.__screen)
        #definindo o turno e seu display
        Viewer.__instance.__turn = Turno(IMAGES_INFO, Viewer.__instance.myfont)
        #definindo os 6 samurais
        Viewer.__instance.__samurais = [Samurai(i, IMAGES, IMAGES_BUTTONS, IMAGES_INFO, Viewer.__instance.myfont) for i in range(6)]
        #definindo as acoes
        Viewer.__instance.__acoes = [Acao(i, IMAGES_BUTTONS) for i in range(11)]
        for acao in Viewer.__instance.__acoes:
            acao.update(Viewer.__instance.__screen)
        #definindo a lista de ordens
        Viewer.__instance.__orderList = OrderList(IMAGES, IMAGES_BUTTONS)
        Viewer.__instance.__orderList.update(Viewer.__instance.__screen)
        #definindo o botão que escolhe o samurai
        Viewer.__instance.__buttonSamurai = ButtonSamurai(IMAGES, IMAGES_BUTTONS, IMAGES_INFO)
        pygame.display.update()
        return Viewer.__instance

    def render(self, message):
        #atualizando o turno atual
        self.__turn.setTurn(message['turn'])

        #atualizando a lista de acoes
        self.__orderList.clear()
        self.__orderList.setSamurai(str(self.__buttonSamurai.num))

        #atualizando o tabuleiro
        self.__board.update(self.__screen, message['board'])

        #atualizando os samurais e colocando eles no tabuleiro
        for samurai in self.__samurais:
            x, y, order_status, hidden, treatment = message['samurais'][samurai.num]
            samurai.update(self.__screen, self.__board, x, y, order_status, hidden, treatment)

        #atualizando o botao que escolhe o samurai com indicador se ele pode jogar
        samurai = self.__samurais[self.__buttonSamurai.num]
        self.__buttonSamurai.update(self.__screen, samurai)
        pygame.display.update()

    @staticmethod
    def close():
        pygame.quit()
        Viewer.__instance = None
