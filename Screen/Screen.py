from pygame.locals import *
import pygame

class Screen:
    screenDict = {}
    game = None
    def __init__(self,name,game):
        print("constructing: ",name)
        if name in Screen.screenDict.keys():
            raise "already exists"
        else:
            Screen.screenDict[name]= self
        Screen.game = game;
    def handleEvent(self,event):
        pass

    def updateScreen(self,delta):
        pass

    def renderScreen(self,screen,delta):
        pass
