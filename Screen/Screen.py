from pygame.locals import *
import pygame
import View.Renderer
import Controller
import Screen.GUI as GUI
class Screen:
    screenDict = {}

    def __init__(self,name):
        print("constructing: ",name)
        if name in Screen.screenDict.keys():
            raise "already exists"
        else:
            Screen.screenDict[name]= self
        self.useRenderer=True
        self.renderer=None
        self.mousepos=(0,0)
        self.mousebut=[False,False,False]
        self.guiObjects = []
        self.Width = 160
        self.Height =90
        self.nextScreen= None
        self.lastMenu = Controller.menuSelector

    def handleEvent(self,event):
        if(event.type ==pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
            self.mouseDriven=True
            Controller.keyboard = False
            Controller.controller = False
            if Controller.inputButtons["debug"]:
                print(event,pygame.mouse.get_pos())
            self.mousepos=(event.pos[0]/View.Renderer.WIDTH_P*self.Width,event.pos[1]/View.Renderer.HEIGHT_P*self.Height)
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button-1 <3):
                    self.mousebut[event.button-1]=True
            if(event.type == pygame.MOUSEBUTTONUP):
                if (event.button-1 < 3):
                    self.mousebut[event.button-1] = False

        if(event.type == pygame.KEYDOWN):
            for guiO in self.guiObjects:
                if (isinstance(guiO, GUI.ButtonMenu)):
                    for b in guiO.buttons:
                        if (isinstance(b, GUI.Input)):
                            print(event)
                            b.updateText(event.unicode)

                if (isinstance(guiO, GUI.Input)):
                    guiO.updateText(event.unicode)

    def changeScreen(self,name=None):
        self.nextScreen = name

    def changeTo(self,game):
        pass
    def updateScreen(self,delta):

        for guiO in self.guiObjects:
            if(isinstance(guiO,GUI.ButtonMenu)):
                for b in guiO.buttons:
                    b.update(self.mousepos, self.mousebut)
            if(isinstance(guiO,GUI.Button)):
                guiO.update(self.mousepos,self.mousebut)

            if (isinstance(guiO, GUI.Input)):
                guiO.update(self.mousepos, self.mousebut)

