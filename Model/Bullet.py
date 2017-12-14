from Model.GameObj import GameObj
from Model.Asteroid import Asteroid
import pygame
import math
class Bullet(GameObj):
    def __init__(self,x,y,speed,angle,owner):
        super().__init__(x,y)
        self.velocity=pygame.math.Vector2(speed,0).rotate(angle);
        self.life = 2
        self.owner=owner
        self.mass=0.01

    def render(self,screen,delta,game):
        pygame.draw.circle(screen,(255,255,255),(math.floor(self.position.x),math.floor(self.position.y)),math.floor(5));

    def onCollide(self,a):
        if(a ==self.owner):
            return
        if(isinstance(a,Bullet)):
            return
        if(isinstance(a,Asteroid)):
            print("Asteroid")
            a.hit=True
        self.alive=False
    def isCollideable(self,a):
        return isinstance(a,Asteroid)
    def getCollider(self):
        return 5;
    def update(self,delta):
        self.life-=delta
        if(self.life<=0):
            self.alive=False
        super().update(delta)