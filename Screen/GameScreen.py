import random

import Controller;
from Model.Asteroid import Asteroid
from Screen.Screen import *
from Model.Ship import Ship
from Model.GameObj import GameObj
from Model.Bullet import Bullet
from Model.Enemy import Enemy
from Model.LootBox import LootBox
import math
import Sound

import View.Renderer
import Files
import View.ScreenRenderer as gui

class GameScreen(Screen):
    def pauseMenu(self,item):
        if(item == "UP"):
            Controller.inputButtons["pause"] = False
        else:
            self.changeScreen(item)
    def __init__(self, game,scale):
        super().__init__("Game")
        self.game = game
        self.renderers=["game","screen"]
        self.renderData["game"]=game


        self.renderer = gui.ScreenRenderer(self.Width, self.Height)

        self.menu = gui.ButtonMenu(70, 30, 25, 7, 1, {
            "Unpause": "UP",
            "Retry": "Game",
            "Main Menu":"Main",
            "Exit": "QUIT",
        }, function=self.pauseMenu, scale=self.renderer.getMP(1))
        self.menu.visible=False
        self.guiObjects.append(self.menu)

    def getAsteroidsToSpawn(self):
        return math.floor(10*(2*(self.game.score/1000) +3))
    def getEnemiesToSpawn(self):
        return self.game.level()**2
    def changeTo(self,game):
        Controller.inputButtons["pause"]=False
        Sound.playMusic("music",fadein=900)

        game.spawnedAsteroids=0
        game.spawnedEnemies=0
        game.addedLife=0

        Asteroid.count=0
        game.ship = Ship(game.WIDTH / 2, game.HEIGHT / 2);  # statek gracza
        game.gameObjects = []  # lista obiektów
        game.gameObjects.append(game.ship)
        game.messages=[]
        # spawnowanie startowych asteroid

        game.score = 0;  # punkty
        game.destroyedAsteroids =0
        game.hp = 3;  # życie

    def spawnAsteroids(self,game):
        while game.spawnedAsteroids < self.getAsteroidsToSpawn():
            if random.random()<0.5:
                pos = (random.random() * game.WIDTH,random.choice([-50-30*random.random(), game.HEIGHT+50+30*random.random()]))
            else:
                pos = (random.choice([-50-30*random.random(), game.WIDTH+50+30*random.random()]),random.random() * game.HEIGHT)

            a = Asteroid(pos[0],pos[1],random.choice(["LARGE","LARGE","LARGE","XLARGE","XLARGE","MEDIUM"]))
            col = False
            for b in game.gameObjects:
                if(a.checkCollision(b)):
                    col = True
                    return

            if not col:
                game.spawnedAsteroids+=1
                game.gameObjects.append(a.add())

    def spawnEnemies(self,game):
        while game.spawnedEnemies < self.getEnemiesToSpawn():
            a = Enemy(random.random() * game.WIDTH, random.random() * game.HEIGHT, game)
            col = False
            for b in game.gameObjects:
                if (a.checkCollision(b)):
                    col = True
                    break

            if not col:
                game.spawnedEnemies += 1
                game.gameObjects.append(a)

    def updateScreen(self,delta):
        super().updateScreen(delta)
        game = self.game
        View.Renderer.DEBUG=Controller.inputButtons["debug"]
        self.menu.visible=Controller.inputButtons["pause"]
        if(Controller.inputButtons["pause"]):

            return
        #print(self.getAsteroidsToSpawn(),self.getEnemiesToSpawn(),self.game.destroyedAsteroids,Asteroid.count)
        if(game.score>game.addedLife*500):
            game.addMsg("Repair Kit Tracking Signal Discovered")
            game.addedLife+=1
            game.gameObjects.append(LootBox(random.random() * game.WIDTH,random.random() * game.HEIGHT,game,type="hp"))

        if(self.getAsteroidsToSpawn()-game.spawnedAsteroids>5  and Asteroid.count <=50):
            self.spawnAsteroids(game)

        if (self.getEnemiesToSpawn()-game.spawnedEnemies>3):
            game.messages.append("Alien contacts incoming")
            self.spawnEnemies(game)

        if(game.ship.coolDown<=0 and Controller.inputButtons["shot"]):
            Sound.playSound("laser")
            b = Bullet(game.ship.position.x,game.ship.position.y,1000,game.ship.rotation,game.ship)
            b.velocity+= game.ship.velocity
            game.gameObjects.append(b)

            game.ship.coolDown=game.ship.maxColdown;

        if(game.ship.hit):
            game.addMsg("Critical Damage!!!")
            game.addMsg("use Repair Kit - press [{:s}]".format(
                pygame.key.name(Controller.keyBindings["Keyboard"][
                                    "revive"]) if Controller.keyboard else "(A)" if Controller.controller else ""
            ))
            game.ship.hit = False

        if (game.ship.dead or game.hp <0):
            game.ship.position.x = -game.WIDTH
            game.ship.position.y = -game.HEIGHT
            if(len(game.messages)<1):
                game.addMsg("use Repair Kit - press [{:s}]".format( pygame.key.name(Controller.keyBindings["Keyboard"][
                                    "revive"]) if Controller.keyboard else "(A)" if Controller.controller else ""
            ))

            if(game.hp >0 and Controller.inputButtons["revive"]):
                Controller.inputButtons["revive"]=False
                Sound.playSound("click")
                Sound.playSound("pickup")
                game.addMsg("Using Repair Kit. [ {:d} left ]".format(game.hp-1))
                game.ship.setDead(False)
                game.ship.inV=3
                game.ship.position.x=game.WIDTH/2
                game.ship.position.y=game.HEIGHT/2
                game.ship.velocity.x = 0
                game.ship.velocity.y = 0
                game.hp-=1
            elif(game.hp <=0):
                Sound.stopMusic(fadeout=5500)
                self.nextScreen="GameOver"


        for (i,gameObject) in enumerate(game.gameObjects):
            if(not gameObject.alive):

                if isinstance(game.gameObjects.pop(i),Asteroid):
                    game.destroyedAsteroids+=1
                continue
            if(isinstance(gameObject,Ship) and gameObject.dead):
                continue

            gameObject.update(delta)
            if(isinstance(gameObject,Asteroid) and gameObject.hit):
                gameObject.crack(game,i);

            if (isinstance(gameObject, Enemy) and gameObject.hit):
                gameObject.destroy(game, i);

            for gameObject2 in game.gameObjects[i+1:]:
                if(gameObject.checkCollision(gameObject2)):
                    gameObject.collide(gameObject2)

            #Ograniczenie planszy

            if(gameObject.position.x<-gameObject.bias):
                gameObject.position.x=game.WIDTH+gameObject.bias;

            if(gameObject.position.x>game.WIDTH+gameObject.bias):
                gameObject.position.x=-gameObject.bias;

            if(gameObject.position.y<-gameObject.bias):
                gameObject.position.y=game.HEIGHT+gameObject.bias;

            if(gameObject.position.y>game.HEIGHT+gameObject.bias):
                gameObject.position.y=-gameObject.bias;


