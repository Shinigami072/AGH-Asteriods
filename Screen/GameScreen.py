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
class GameScreen(Screen):

    def __init__(self, game):
        super().__init__("Game")
        self.game = game
        self.useRenderer=True;
        self.renderer=None
        self.spawnedAsteroids=0
        self.spawnedEnemies=0
        self.addedLife=0

    def getAsteroidsToSpawn(self):
        return math.floor(20*(2*(self.game.score/1000) +1))
    def getEnemiesToSpawn(self):
        return math.floor(self.game.destroyedAsteroids/150)**2+40
    def handleEvent(self,event):
        #print(event)
        #Controller.eventHandle(event)
        pass
    def changeTo(self,game):
        Sound.playMusic("music",fadein=900)

        self.spawnedAsteroids=0
        self.spawnedEnemies=0
        Asteroid.count=0
        game.ship = Ship(game.WIDTH / 2, game.HEIGHT / 2);  # statek gracza
        game.gameObjects = []  # lista obiektów
        game.gameObjects.append(game.ship)
        # spawnowanie startowych asteroid

        game.score = 0;  # punkty
        game.destroyedAsteroids =0
        game.hp = 3;  # życie

    def spawnAsteroids(self,game):
        while self.spawnedAsteroids < self.getAsteroidsToSpawn():
            if random.random()<0.5:
                pos = (random.random() * game.WIDTH,random.choice([5*random.random(), game.HEIGHT-5*random.random()]))
            else:
                pos = (random.choice([5*random.random(), game.WIDTH-5*random.random()]),random.random() * game.HEIGHT)

            a = Asteroid(pos[0],pos[1],random.choice(["LARGE","LARGE","LARGE","XLARGE","XLARGE"]))
            col = False
            for b in self.guiObjects:
                if(a.checkCollision(b)):
                    col = True
                    break

            if not col:
                self.spawnedAsteroids+=1
                game.gameObjects.append(a.add())
    def spawnEnemies(self,game):
        while self.spawnedEnemies < self.getEnemiesToSpawn():
            a = Enemy(random.random() * game.WIDTH, random.random() * game.HEIGHT, game)
            col = False
            for b in self.guiObjects:
                if (a.checkCollision(b)):
                    col = True
                    break

            if not col:
                self.spawnedEnemies += 1
                game.gameObjects.append(a)

    def updateScreen(self,delta):
        game = self.game
        View.Renderer.DEBUG=Controller.inputButtons["debug"]
        if(Controller.inputButtons["pause"]):
            return
        #print(self.getAsteroidsToSpawn(),self.getEnemiesToSpawn(),self.game.destroyedAsteroids,Asteroid.count)
        if(game.score>self.addedLife*1000):
            print("ExtraLife\n\n\n\n\n\n")
            self.addedLife+=1
            game.gameObjects.append(LootBox(random.random() * game.WIDTH,random.random() * game.HEIGHT,game))
        if(self.spawnedAsteroids< self.getAsteroidsToSpawn() and Asteroid.count <=50):
            self.spawnAsteroids(game)

        if (self.spawnedEnemies < self.getEnemiesToSpawn()):
            self.spawnEnemies(game)

        if (Controller.inputButtons["inV"]):
            game.ship.inV+=delta*10

        if(game.ship.coolDown<=0 and Controller.inputButtons["shot"]):
            Sound.playSound("laser")
            b = Bullet(game.ship.position.x,game.ship.position.y,1000,game.ship.rotation,game.ship)
            b.velocity+= game.ship.velocity
            game.gameObjects.append(b)

            game.ship.coolDown=game.ship.maxColdown;



        if (game.ship.dead or game.hp <0):
            if(game.hp >0):
                game.ship.setDead(False)
                game.ship.inV=3
                game.ship.position.x=game.WIDTH/2
                game.ship.position.y=game.HEIGHT/2
                game.ship.velocity.x = 0
                game.ship.velocity.y = 0
                game.hp-=1
            else:
                Sound.stopMusic(fadeout=5500)
                self.nextScreen="GameOver"


        for (i,gameObject) in enumerate(game.gameObjects):
            if(not gameObject.alive):

                if isinstance(game.gameObjects.pop(i),Asteroid):
                    game.destroyedAsteroids+=1
                print("rmove ",i)
                continue
            gameObject.update(delta)
            if(isinstance(gameObject,Asteroid) and gameObject.hit):
                gameObject.crack(game,i);

            if (isinstance(gameObject, Enemy) and gameObject.hit):
                gameObject.destroy(game, i);

            for gameObject2 in game.gameObjects[i+1:]:
                if(gameObject.checkCollision(gameObject2) and gameObject.isCollideable(gameObject2) and gameObject2.isCollideable(gameObject)):
                    gameObject.collide(gameObject2)

            if(gameObject.position.x<0):
                gameObject.position.x=game.WIDTH;

            if(gameObject.position.x>game.WIDTH):
                gameObject.position.x=0;

            if(gameObject.position.y<0):
                gameObject.position.y=game.HEIGHT;

            if(gameObject.position.y>game.HEIGHT):
                gameObject.position.y=0;


