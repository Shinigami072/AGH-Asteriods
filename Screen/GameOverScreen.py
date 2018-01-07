import pygame
from Screen.Screen import Screen
import View.ScreenRenderer as gui
import HighScore
import random
import Controller
import Sound
import Screen.GUI as GUI
import Files
class GameOverScreen(Screen):


    def __init__(self,hiscore):
        super().__init__("GameOver")
        self.useRenderer=False
        self.renderer = gui.ScreenRenderer(self.Width ,self.Height )

        menu = gui.ButtonMenu(15, 5, 25, 7, 1, {
            "Retry": "Game",
            "High Score":"HiScore",
            "Main Menu": "Main"
        }, function=self.changeScreen, scale=self.renderer.getMP(1))
        self.inputbox=GUI.Input("PLAYER",90,5,67,7,id=1,menuCount=6,maxwidth=13,font="mono-72")
        menu.add(self.inputbox)

        self.guiObjects.append(menu)

        self.s = gui.StringC("You Got [HI SCORE]!",50,6)
        self.guiObjects.append(self.s)
        self.hiScoreT=hiscore
        self.newScore=None


    def changeTo(self,game):
        self.hiScoreT.read()

        if Sound.musicChannel.get_sound() != Sound.getSound("m_menu"):
            Sound.playMusic("m_menu",fadeout=5000)
        self.newScore=HighScore.HighScore(random.choice(Files.NAMES), game.score)

        if(self.hiScoreT.lowscore < self.newScore.score):

            self.s.string="GAME OVER:\n\n         " \
                          "Congratulations:\n\n         " \
                          "You set a new High Score {}!!!!\n\n         " \
                          "Current High Score: {}".format(game.score,self.hiScoreT.highscore)
            self.inputbox.visible=True
            self.inputbox.string.string = self.newScore.name

        else:
            self.inputbox.visible=False
            self.s.string="GAME OVER:\n\n         " \
                          "You scored: {}\n\n         " \
                          "You need to score more than {} to be remembered.\n\n         " \
                          "Current High Score: {}".format(game.score,self.hiScoreT.highscore,self.hiScoreT.highscore)


    def changeScreen(self,name):
        print("changeMain")
        self.nextScreen = "Main"
        if(self.newScore is not None and self.inputbox.visible):
            self.newScore.name = self.inputbox.string.string
            self.hiScoreT.add(self.newScore)
            self.hiScoreT.write()

        super().changeScreen(name)



