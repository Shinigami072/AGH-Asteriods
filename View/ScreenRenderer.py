import View.Renderer
import pygame
import math
import random
import Files
import Sound
import Controller
from Screen.GUI import *

class ScreenRenderer(View.Renderer.Renderer):
    def __init__(self,width,height):
        super().__init__(width,height)

    def renderString(self,string):
        dy =0
        self.font = Files.FONTS[string.font]
        for strin in string.string.split("\n"):
            if(len(strin.strip()) >0):
                self.screen.blit(self.font.render(strin, True,
                        string.color if strin.strip()[0]!='#' else View.Renderer.DEBUG_PURPLE),
                        (self.getMP(string.x), self.getMP(string.y+dy)))
            dy+=string.height
    def renderButton(self,button):
        width =0
        if(button.state==0):
            width=3
        pygame.draw.rect(self.screen,
                         button.color,
                         pygame.Rect(self.getMP(button.x),self.getMP(button.y),self.getMP(button.width),self.getMP(button.height)), width
                         )
        self.renderString(button.string)

    def renderButtons(self,buttonmenu):
        for b in buttonmenu.buttons:
            self.renderButton(b)
    def render(self,screen,delta):
        #self.screen.fill(View.Renderer.BLACK)
        for guiEl in screen.guiObjects:
            if(not guiEl.visible):
                continue
            if( isinstance(guiEl,StringC)):
                self.renderString(guiEl)
            if (isinstance(guiEl, Button)):
                self.renderButton(guiEl)
            if (isinstance(guiEl, Input)):
                self.renderButton(guiEl)
            if (isinstance(guiEl, ButtonMenu)):
                self.renderButtons(guiEl)
