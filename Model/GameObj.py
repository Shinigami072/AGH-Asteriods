import pygame
import View.Particles
import random
import math
#m - kg
#V - m/s

#podstawowy obiekt - posiada dane porzebne dla fukcjonowanie fizyki
#i podstawowego renderowania
class GameObj:
    def __init__(self,x,y):
        self.position =pygame.math.Vector2(x,y)
        self.velocity =pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.particleEmitters = {}
        self.rotation = 0
        self.scale = 1
        self.modelScale=1
        self.rotVel =0;
        self.maxAccel=50;
        self.mass=1;
        self.alive = True
        self.model=None
        self.harmful=True
        self.emitterGroups={}

    def setModel(self,model):
        self.model=model
        self.particleEmitters = {}
        self.emitterGroups=model.particleGroups
        for PED in self.model.particleEmitters:
            self.particleEmitters[PED]= self.model.particleEmitters[PED].getParticleEmitter(self)

    def setGroupActive(self,group : str,active : bool,override : bool = False):
        for emit in self.emitterGroups[group]:
            if not override:
                self.particleEmitters[emit].active=active or self.particleEmitters[emit].active
            else:
                self.particleEmitters[emit].active=active

    def getQuickestRot(self, rot):
        Qrot = rot - self.rotation
        if (math.fabs(Qrot) <= 180):
            return Qrot
        if (rot < self.rotation):
            return (360 + rot) - self.rotation

        if (rot > self.rotation):
            return rot - (self.rotation + 360)

    def updateMotion(self,delta: float):
        self.rotation += self.rotVel*delta
        self.velocity += self.acceleration*delta;
        self.position += self.velocity*delta;

        if (self.rotation < 0):
            self.rotation = self.rotation + 360
        if (self.rotation >= 360):
            self.rotation = self.rotation - 360
        pass

    def getCollider(self):
        return None
    def onCollide(self,a):
        pass
    def render(self,screen,delta,game):
        pass
    def isCollideable(self,a):
        return True

    def isInteractable(self, a):
        return True

    def collide(self,a):
        a.onCollide(self)
        self.onCollide(a)
        if not (self.isInteractable(a) and a.isInteractable(self)):
            return
        aVelocity_mps = ((self.mass-a.mass)*self.velocity + 2*a.mass*a.velocity)/(self.mass+a.mass);
        bVelocity_mps = ((a.mass-self.mass)*a.velocity + 2*self.mass*self.velocity)/(self.mass+a.mass);

        penDist_m = -((self.position-a.position).length()-(self.getCollider()+a.getCollider()))
        if(self.velocity != a.velocity):
            penTime_s = penDist_m/(self.velocity-a.velocity).length()
        else:
            penTime_s=0

        self.position -= self.velocity*penTime_s
        a.position -= a.velocity*penTime_s

        self.position += aVelocity_mps*penTime_s
        a.position += bVelocity_mps*penTime_s

        self.velocity = aVelocity_mps
        a.velocity = bVelocity_mps



    def checkCollision(self, a):
            if None is self.getCollider() or a.getCollider() is None or not self.alive or not a.alive:
                return False
            diff = self.position-a.position
            dist = (self.getCollider()+a.getCollider())**2
            collided = diff.length_squared()<=dist
            return collided

    def update(self,delta):
            self.updateMotion(delta)

