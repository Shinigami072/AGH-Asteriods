#! /usr/bin/python3
from Screen.CreditsScreen import *
from Screen.GameOverScreen import GameOverScreen
from Screen.HiscoreScreen import HiScoreScreen
from Screen.GameScreen import *
from Screen.MainScreen import *
from HighScore import HighScores
import View.Renderer as Renderer
from  Model.Ship import Ship
import Files
import random
from Screen.ModelScreen import ModelScreen

#dane Gry
class GameData:
    def __init__(self):
        self.WIDTH = 3200 #rozmiar planszy
        self.HEIGHT = 1800
        self.ship = Ship(self.WIDTH/2,self.HEIGHT/2); #statek gracza
        self.gameObjects = [] #lista obiektów
        self.gameObjects.append(self.ship)
        self.score = 0; #punkty
        self.destroyedAsteroids = 0
        self.hp = 3; #życie

class App:

    def __init__(self):
        print("constructor")
        self.renderer = None; #ustawienie Renderera
        self.GameData = None #ustawienie Danych gry
        self.current_screen = None #ustawienie obecnego ekranu
        self.prev_screen = None
        self.done = False #ustawienie wyjścia z gry

    def init(self):
        print("Game init")
        pygame.mixer.pre_init(48000, 16, 2, 4096)
        pygame.init()
        Sound.init()
        Files.loadData()
        self.GameData = GameData()
        self.renderer=Renderer.VectorRenderer(self.GameData.WIDTH,self.GameData.HEIGHT)
       # Files.FONTS["default"] = Files.FONTS["cow-72"]#pygame.font.SysFont(pygame.font.get_default_font(), 72)
      #  Renderer.Renderer.fonts["mono-72"]=pygame.font.Font("files/joystix monospace.ttf",72)
       # Renderer.Renderer.fonts["mono-36"]=pygame.font.Font("files/joystix monospace.ttf",36)
        #Renderer.Renderer.fonts["mono-12"]=pygame.font.Font("files/joystix monospace.ttf",12)
        #print(Renderer.Renderer.fonts)
        if(pygame.joystick.get_count() >0):#sprawdzenie czy jest podpięty i ustawienie GamePada
            pygame.joystick.Joystick(0).init();
            Controller.keyboard=False

        self.done = False
        self.current_screen = GameScreen(self.GameData) #ustawienie ekranu
        self.current_screen = MainScreen();
        h = HighScores()
        h.read()
        h.write()
        print(h)
        CreditsScreen()
        HiScoreScreen(h)
        GameOverScreen(h)
        ModelScreen()
        return True

    def cleanup(self):
        print("Cleanup")#wyczysczenie używanych zasobów
        pygame.quit()

    def main(self):
        print("main-func")
        if not self.init():
            self.done = True

        while not self.done:

            delta = self.renderer.clock.tick(Renderer.FPS)/1000
            #delta - czas jaki upłynoł od ostatniej aktualizacji gry w sekundach

            for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    self.done = True
                Controller.eventHandle(event) #translacja eventów na sposób kontroli
                self.current_screen.handleEvent(event)#zajęcie się wszyskimi eventami
            Controller.handleRotation(Controller.inputRotation+Controller.rotKey*270*delta)
            self.current_screen.updateScreen(delta) #aktualizacja obecnego ekranu

            if(self.current_screen.nextScreen):#system zmiany ekranów
                if(self.current_screen.nextScreen == "QUIT"):
                    self.done=True;
                    continue
                self.prev_screen = self.current_screen
                self.current_screen= Screen.screenDict[self.current_screen.nextScreen]
                self.current_screen.changeTo(self.GameData)
                self.prev_screen.nextScreen = None

            if(self.current_screen.useRenderer):
                self.renderer.DEBUG = Controller.inputButtons["debug"]  # ustwaienie opcji debug w rendererze
                self.renderer.render(self.GameData,delta)

            if(self.current_screen.renderer):
                self.current_screen.renderer.DEBUG = Controller.inputButtons["debug"]  # ustwaienie opcji debug w rendererze
                self.current_screen.renderer.render(self.current_screen,delta) #użycie innego renderera

            pygame.display.flip()
            self.renderer.screen.fill(Renderer.BLACK)

            #  self.renderer.screen.blit( self.lastScreen,(0,self.y));
            #self.current_screen.renderScreen(self.screen,delta)

        self.cleanup()#wyczyszczenie po grze


#Start App
if __name__ =="__main__":
    app = App()
    app.main()