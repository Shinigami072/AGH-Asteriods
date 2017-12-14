import pygame

FPS = 60
HEIGHT_P = 720
WIDTH_P = 1280
M_TO_P = 10

class Renderer:
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_P, HEIGHT_P))

    def render(self,game):
        pass


