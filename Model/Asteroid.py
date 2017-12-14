import pygame
import math
import random
from Model.GameObj import GameObj as GameObj

from pygame.math import Vector2

ASTEROID_SIZE = 60
class Asteroid(GameObj):
    def __init__(self,x,y):
        super().__init__(x,y);
        self.velocity =pygame.math.Vector2(random.random()*150,random.random()*150)
        self.size = random.random()*0.9+0.1
        self.mass = 10*self.size
        self.hit = False

    def drawAt(self,x,y,screen,delta):
        pygame.draw.circle(screen,(255,255,255),(math.floor(x),math.floor(y)),math.floor(self.size*ASTEROID_SIZE));

    def render(self,screen,delta,game):
        self.drawAt(self.position.x,self.position.y,screen,delta)
        pygame.draw.aaline(screen,(0,220,220),(self.position.x,self.position.y),(self.position.x+self.velocity.x,self.position.y+self.velocity.y))


    def getCollider(self):
        return self.size*ASTEROID_SIZE

    def isInside(self,x,y,radius):
        pos2 = pygame.math.Vector2(x,y)
        dist = pos2-self.position

        return (dist.length()<radius+self.size*ASTEROID_SIZE)