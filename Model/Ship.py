import pygame
import math
import Controller
from Model.GameObj import GameObj as GameObj

class Ship(GameObj):
    def __init__(self,x,y):
        super().__init__(x,y);
        self.rotation = 0
        self.maxRotation =200;
        self.maxAccel=50;
        self.size = 0.2
        self.coolDown = 0;
        self.maxColdown =0.5;

    def drawAt(self,x,y,screen,delta):
        pygame.draw.polygon(screen,(255,255,255),
                            ((x+self.size*80*math.cos(math.radians(self.rotation)),y+self.size*80*math.sin(math.radians(self.rotation))),
                             (x+self.size*40*math.cos(math.radians(self.rotation+120)),y+self.size*40*math.sin(math.radians(self.rotation+120))),
                             (x,y),
                             (x+self.size*40*math.cos(math.radians(self.rotation-120)),y+self.size*40*math.sin(math.radians(self.rotation-120)))))

    def render(self,screen,delta,game):
        self.drawAt(self.position.x,self.position.y,screen,delta)
        self.drawAt(self.position.x+game.size[0],self.position.y,screen,delta)
        self.drawAt(self.position.x-game.size[0],self.position.y,screen,delta)
        self.drawAt(self.position.x,self.position.y+game.size[1],screen,delta)
        self.drawAt(self.position.x,self.position.y-game.size[1],screen,delta)
        pygame.draw.aaline(screen,(0,220,220),(self.position.x,self.position.y),(self.position.x+self.velocity.x,self.position.y+self.velocity.y))
        pygame.draw.circle(screen,(0,220,220),(math.floor(self.position.x),math.floor(self.position.y)),math.floor(self.getCollider()),1)

    def getCollider(self):
        return 10

    def onCollide(self,a):
        print("Ship Cosllison Detected",type(a))


    def update(self,delta):
        if(self.coolDown>0):
            self.coolDown-=delta
        if(self.coolDown<0):
            self.coolDown=0;

        self.rotation += Controller.inputVector.x*self.maxRotation*delta
        if Controller.inputVector.y > 0:
            self.acceleration = self.maxAccel*Controller.inputVector.y*pygame.math.Vector2(1, 0).rotate(self.rotation)
        else:
            if self.velocity.x == 0 and self.velocity.y ==0:
                self.acceleration=self.acceleration*0
            else:
                self.acceleration = self.maxAccel*Controller.inputVector.y*self.velocity.normalize()

        GameObj.updateMotion(self,delta)

