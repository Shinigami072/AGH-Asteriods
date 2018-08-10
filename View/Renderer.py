import pygame

FPS = 60
#HEIGHT_P = 720
#WIDTH_P = 1280
HEIGHT_P = 1080
WIDTH_P = 1920

BLACK = pygame.math.Vector3(0,0,0)
GRAY = pygame.math.Vector3(90,90,90)
WHITE = pygame.math.Vector3(255,255,255)
DEBUG_BLUE = pygame.math.Vector3(0,220,220)
DEBUG_PURPLE = pygame.math.Vector3(220,0,220)
DEBUG_YELLOW = pygame.math.Vector3(220,220,0)

import pygame.gfxdraw

#
#klasa rozdzielająca gamespace i screenspace
#zajmuje się całóścią renderowania

class Renderer:
    def __init__(self,width,height):
        global WIDTH_P
        global HEIGHT_P

        self.M_TO_P = max((width)/WIDTH_P,(height)/HEIGHT_P)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_P, HEIGHT_P))
        self.DEBUG = False

    def render(self,game,delta):
        pass

    def getMP(self,m):
        return m / self.M_TO_P

    def getMPPos(self,m):
        return self.getMP(m)


