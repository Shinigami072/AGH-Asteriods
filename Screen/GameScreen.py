import random

import Controller;
from Model.Asteroid import Asteroid
from Screen.Screen import *
from Model.GameObj import GameObj
from Model.Bullet import Bullet
import View.Renderer

class GameScreen(Screen):

    def __init__(self, game):
        self.game = game

    def renderScreen(self,screen,delta):
        #self.ship.render(screen,delta,self.game)
        pass


    def handleEvent(self,event):
        #print(event)
        Controller.eventHandle(event)

    def updateScreen(self,delta):
        game = self.game
        if(Controller.inputButtons["debug"]):
            View.Renderer.DEBUG=not View.Renderer.DEBUG;
            Controller.inputButtons["debug"] = False
        if (Controller.inputButtons["inV"]):
            game.ship.inV+=delta*10
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
        if(game.ship.coolDown<=0 and Controller.inputButtons["shot"]):
            game.gameObjects.append(Bullet(game.ship.position.x,game.ship.position.y,500,game.ship.rotation,game.ship))
            game.ship.coolDown=game.ship.maxColdown;



        if (game.ship.dead):
            if(game.hp >0):
                game.ship.dead=False
                game.ship.inV=3
                game.ship.position.x=game.WIDTH/2
                game.ship.position.y=game.HEIGHT/2
                game.ship.velocity.x = 0
                game.ship.velocity.y = 0
                game.hp-=1


        for (i,gameObject) in enumerate(game.gameObjects):
            if(not gameObject.alive):
                game.gameObjects.pop(i)
                print("rmove ",i)
                continue
            gameObject.update(delta)
            if(isinstance(gameObject,Asteroid) and gameObject.hit):
                gameObject.crack(game,i);

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



