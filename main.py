#! /usr/bin/python3
from Screen.CreditsScreen import CreditsScreen
from Screen.GameOverScreen import GameOverScreen
from Screen.HiscoreScreen import HiScoreScreen
from Screen.GameScreen import GameScreen
from Screen.MainScreen import MainScreen
from Screen.ModelScreen import ModelScreen
from Screen.OptionsScreen import OptionScreen
from Screen.Screen import Screen

from HighScore import HighScores

import View.Renderer as Renderer
import View.GameRenderer
import View.ScreenRenderer

from  Model.Ship import Ship
import Files
import Sound
import Controller
import pygame


#dane Gry
class GameData:
    def __init__(self):
        self.WIDTH = 3200 #rozmiar planszy
        self.HEIGHT = 1800
        self.ship = None #statek gracza
        self.gameObjects = [] #lista obiektów
        self.score = 0; #punkty
        self.destroyedAsteroids = 0
        self.hp = 3; #życie
        self.spawnedAsteroids = 0
        self.spawnedEnemies = 0
        self.addedLife = 0
        self.messages = []
        self.msgTimer = 1
    def level(self):
        return self.destroyedAsteroids//50
    def addMsg(self,str):
        self.messages.append(str)
        if(len(self.messages) >3):
            self.messages.pop(0)

class App:

    def __init__(self):
        print("constructor")
        self.renderers = None; #ustawienie Renderera
        self.GameData = None #ustawienie Danych gry
        self.current_screen = None #ustawienie obecnego ekranu
        self.prev_screen = None
        self.done = False #ustawienie wyjścia z gry
        self.clock = None


    def init(self):

        print("Game init")
        pygame.mixer.pre_init(48000, 16, 2, 4096)
        pygame.init()
        self.clock = pygame.time.Clock()
        Sound.init()
        Files.loadData() #załadowanie plików

        self.GameData = GameData()

        self.renderers={
            "game":View.GameRenderer.VectorRenderer(self.GameData.WIDTH,self.GameData.HEIGHT),
            "screen":View.ScreenRenderer.ScreenRenderer(160,90),
        }

        if pygame.joystick.get_count() >0:#sprawdzenie czy jest podpięty i ustawienie GamePada
            pygame.joystick.Joystick(0).init();
            Controller.keyboard=False
            Controller.controller=True

        self.done = False
        self.current_screen = GameScreen(self.GameData,self.renderers["screen"].getMP(1)) #ustawienie ekranu
        self.current_screen = MainScreen(self.renderers["screen"].getMP(1));

        #załadowanie wyników
        h = HighScores()
        h.read()
        h.write()
        print(h)

        #inicjalizacja ekranów
        CreditsScreen(self.renderers["screen"].getMP(1))
        HiScoreScreen(h,self.renderers["screen"].getMP(1))
        GameOverScreen(h,self.renderers["screen"].getMP(1))
        ModelScreen()
        OptionScreen(self.renderers["screen"].getMP(1))

        return True



    def main(self):
        print("main-func")
        if not self.init():
            self.done = True

        while not self.done:

            delta = self.clock.tick(Renderer.FPS)/1000
            #delta - czas jaki upłynął od ostatniej aktualizacji gry w sekundach

            for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    self.done = True
                Controller.eventHandle(event) #translacja eventów na sposób kontroli
                self.current_screen.handleEvent(event)#zajęcie się wszyskimi eventami

            Controller.handleRotation(Controller.inputRotation+Controller.rotKey*600*delta)

            self.current_screen.updateScreen(delta) #aktualizacja obecnego ekranu

            if(self.current_screen.nextScreen):#system zmiany ekranów
                if(self.current_screen.nextScreen == "QUIT"):
                    self.done=True;
                    continue

                self.prev_screen = self.current_screen
                self.current_screen= Screen.screenDict[self.current_screen.nextScreen]
                self.current_screen.changeTo(self.GameData)
                self.prev_screen.nextScreen = None

            for r in self.current_screen.renderers:
                self.renderers[r].DEBUG = Controller.inputButtons["debug"]  # ustwaienie opcji debug w rendererze
                self.renderers[r].render(self.current_screen.renderData[r],delta)


            pygame.display.flip()#zamienienie buforów
            self.renderers["screen"].screen.fill(Renderer.BLACK)


        pygame.quit()#wyczyszczenie po grze


#Start App
if __name__ =="__main__":
    app = App()
    app.main()