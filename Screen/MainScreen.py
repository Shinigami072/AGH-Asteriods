import pygame
from Screen.Screen import *

BUTTON_HEIGHT = 60;
BUTTON_WIDTH = 600;
BUTTON_PAD = 10;
BUTTON_SELECTED = (200,200,200)
BUTTON_DESELECTED = (130,130,130)

class MainScreen(Screen):

    def __init__(self, game):
        super().__init__("Main",game)
        self.selected=0;
        self.Menu = ["Start","Options","Quit"]
        self.Menu_L = len(self.Menu)

    def renderScreen(self,screen,delta):

        for (i,menu_item) in enumerate(self.Menu):
            pygame.draw.rect(screen, BUTTON_SELECTED if i==self.selected else BUTTON_DESELECTED , pygame.Rect((self.game.size[0]-BUTTON_WIDTH)/2 , (self.game.size[1]-(BUTTON_HEIGHT+BUTTON_PAD)*self.Menu_L)+i*(BUTTON_PAD+BUTTON_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT))

    def handleEvent(self,event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP or event.key == pygame.K_w):
                self.selected= (self.selected-1)%self.Menu_L
            if(event.key == pygame.K_DOWN or event.key == pygame.K_s):
                self.selected= (self.selected+1)%self.Menu_L
            if(event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN):
                self.game.next_screen = Screen.screenDict[self.Menu[self.selected]]
            print(event.key)
