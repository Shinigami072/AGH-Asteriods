import pygame
from Screen.Screen import Screen
import View.ScreenRenderer as gui
import HighScore
import Sound
import Controller

class HiScoreScreen(Screen):

    def __init__(self,hiscores):
        super().__init__("HiScore")
        self.useRenderer=False
        self.renderer = gui.ScreenRenderer(self.Width ,self.Height )

        menu = gui.ButtonMenu(15, 5, 25, 7, 1, {
            "Main Menu": "Main"
        }, function=self.changeScreen, scale=self.renderer.getMP(1))
        self.guiObjects.append(menu)

        self.hiScoreT=hiscores

        self.hiScores = gui.StringC(hiscores.__str__(),55,5,font="mono-36")
        self.guiObjects.append(self.hiScores)


    def changeTo(self,game):
        self.hiScoreT.write()
        self.hiScores.string=self.hiScoreT.__str__()

        if Sound.musicChannel.get_sound() != Sound.getSound("m_menu"):
            Sound.playMusic("m_menu")

    def handleEvent(self,event):
        super().handleEvent(event)
        pass

