import random

import Controller;
from Model.Asteroid import Asteroid
from Screen.Screen import *
from Model.GameObj import GameObj
from Model.Bullet import Bullet

class GameScreen(Screen):

    def __init__(self, game):
        super().__init__("Start",game)
        self.ship = Ship(game.width/2,game.height/2);
        self.gameObjects =[]
        self.gameObjects.append(self.ship)
        for i in range(20):
            self.gameObjects.append(Asteroid(random.random()*game.width,random.random()*game.height))
        self.game = game
        self.score =0;

    def renderScreen(self,screen,delta):
        #self.ship.render(screen,delta,self.game)
        for gameObject in self.gameObjects:
            gameObject.render(screen,delta,self.game)


    def handleEvent(self,event):
        #print(event)
        Controller.eventHandle(event)

    def updateScreen(self,delta):
        # self.ship.update(delta)
        # if(self.ship.position.x<0):
        #     self.ship.position.x=self.game.size[0];
        #
        # if(self.ship.position.x>self.game.size[0]):
        #     self.ship.position.x=0;
        #
        # if(self.ship.position.y<0):
        #     self.ship.position.y=self.game.size[1];
        #
        # if(self.ship.position.y>self.game.size[1]):
        #     self.ship.position.y=0;
        if(self.ship.coolDown<=0 and Controller.inputButtons["shot"]):
            self.gameObjects.append(Bullet(self.ship.position.x,self.ship.position.y,500,self.ship.rotation,self.ship))
            self.ship.coolDown=self.ship.maxColdown;

        for (i,gameObject) in enumerate(self.gameObjects):
            if(not gameObject.alive):
                self.gameObjects.pop(i)
                print("rmove ",i)
                continue
            gameObject.update(delta)
            if(isinstance(gameObject,Asteroid) and gameObject.hit):
                gameObject.alive = False
                self.score+=1;
                if(gameObject.size/2 >0.05):
                    aster1 = Asteroid(gameObject.position.x,gameObject.position.y)
                    aster1.mass = gameObject.mass/2
                    aster1.size = gameObject.size/2
                    aster1.velocity = gameObject.velocity.rotate(90)/2

                    aster2 = Asteroid(gameObject.position.x,gameObject.position.y)
                    aster2.mass = gameObject.mass/2
                    aster2.size = gameObject.size/2
                    aster2.velocity = -aster1.velocity

                    self.gameObjects.append(aster1)
                    self.gameObjects.append(aster2)

            for gameObject2 in self.gameObjects[i+1:]:
                if(gameObject.checkCollision(gameObject2) and gameObject.isCollideable(gameObject2) and gameObject2.isCollideable(gameObject)):
                    gameObject.collide(gameObject2)

                if(gameObject.position.x<0):
                    gameObject.position.x=self.game.size[0];

                if(gameObject.position.x>self.game.size[0]):
                    gameObject.position.x=0;

                if(gameObject.position.y<0):
                    gameObject.position.y=self.game.size[1];

                if(gameObject.position.y>self.game.size[1]):
                    gameObject.position.y=0;



