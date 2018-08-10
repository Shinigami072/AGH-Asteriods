from Model.GameObj import GameObj
from Model.Asteroid import Asteroid
from Model.Ship import Ship
import Model.Enemy
import pygame

class Bullet(GameObj):
    def __init__(self,x,y,speed,angle,owner=None,life=2):
        super().__init__(x,y)
        self.velocity=pygame.math.Vector2(speed,0).rotate(angle);
        self.life = life
        self.owner=owner
        self.mass=250

    def onCollide(self,a):
        print(a)
        if(a ==self.owner):
            return
        if(isinstance(a,Bullet)):
            return
        if(isinstance(a,Asteroid) and not isinstance(self.owner,Model.Enemy.Enemy)):
            print("Asteroid")
            a.hit=True
        if (isinstance(a, Model.Enemy.Enemy) and not isinstance(self.owner, Model.Enemy.Enemy)):
            print("Enemy")
            a.hit = True
        if (isinstance(a, Ship)):
            print("Ship")
            a.dead =True

        self.alive=False

    def isCollideable(self,a):
        return ( isinstance(a,Asteroid) or isinstance(a,Model.Enemy.Enemy) and not isinstance(self.owner,Model.Enemy.Enemy)) or (isinstance(a, Ship) and not isinstance(self.owner,Ship))
    def getCollider(self):
        return 5;
    def update(self,delta):
        self.life-=delta
        if(self.life<=0):
            self.alive=False
        super().update(delta)