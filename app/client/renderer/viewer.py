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
    def __new__(cls, player):
        if not Window.__instance:
            Window.__instance = super().__new__(cls)
            pygame.init()
            #definindo a surface
            Window.__instance.__screen = pygame.display.set_mode((800,600))
            Window.__instance.myfont = pygame.font.SysFont("arial", 15)
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
                    Window.__instance.__screen.blit(bg, bg.get_rect())
                    pygame.display.update()
                    pygame.time.delay(2000)

            Window.__instance.__screen.fill([220,220,220])
            pygame.display.update()

        #definindo se o player é o Player 1 ou o Player 2
        Window.__instance.player = player
        #definindo o tabuleiro
        Window.__instance.__board = Board(settings.size)
        #definindo o turno e seu display
        Window.__instance.__turn = Turno()
        #definindo os 6 samurais
        Window.__instance.__samurais = [Samurai(i) for i in range(6)]
        #definindo as acoes
        Window.__instance.__acoes = [Acao(i) for i in range(11)]
        #definindo a lista de ordens
        Window.__instance.__orderList = OrderList(IMAGES, IMAGES_BUTTONS)
        #definindo o botão que escolhe o samurai
        Window.__instance.__buttonSamurai = ButtonSamurai()
        return Window.__instance

    def render(self, mensagem):
        screen = Viewer.__instance.__screen
        Window.__instance.__board.draw(screen)
        pass

    @staticmethod
    def close():
        pygame.quit()
        Window.__instance = None
