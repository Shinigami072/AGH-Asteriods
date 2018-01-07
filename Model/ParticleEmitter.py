import pygame
import random
import math
import View.Particles
class ParticleEmitter:
    def __init__(self,parent,x,y):
        self.position =pygame.math.Vector2(x,y)
        self.parent=parent
        self.active = True
        self.emitCount =5
        self.emitCooldown=0.01;
        self.emitCooldownMax=0.1;
    def getPosition(self):
        if(self.parent):
            rot = math.radians(-self.parent.rotation)
            return self.parent.position+pygame.math.Vector2(
                (math.cos(rot) * self.position.x - math.sin(rot) * self.position.y) *self.parent.scale*self.parent.modelScale,
                - (math.cos(rot) * self.position.y + math.sin(rot) * self.position.x) * self.parent.scale*self.parent.modelScale)
        else:
            return self.position

    def update(self, delta):
        if(self.active):
            if (self.emitCooldown > 0):
                self.emitCooldown -= delta
            else:
                self.emitCooldown = self.emitCooldownMax

    def getParticle(self):
        if ((not self.active or self.emitCooldown > 0)):
            return None
        pos = self.getPosition()
        p =View.Particles.Particle(pos.x,pos.y,maxlife=3+2.7*random.random())
        p.velocity=self.parent.velocity - 0.5*self.parent.velocity.rotate(random.randrange(-10,10))*random.random()
        return p
class Thruster(ParticleEmitter):
    def __init__(self, parent,x,y,rot,rotsize,size,scale):
        super().__init__(parent,x, y)
        self.rot=rot
        self.rotsize=rotsize
        self.emitCount = size
        self.scale=scale
        self.emitCooldownMax = 0
        self.active=False

    def getParticle(self):
        if ((not self.active or self.emitCooldown > 0)):
            return None
        pos = self.getPosition()
        #trans = pygame.math.Vector2(self.size * (0.01 + 0.9 * random.random()), 0).rotate(self.rot);
        part = View.Particles.ParticleThruster(pos.x, pos.y, self.parent,
                                               rotation=(self.rot+(random.choice([-1,1])*random.random()*self.rotsize)),
                                               scale=self.scale*self.parent.thrustScale
                                               )
        #(self, x, y, ship, rotation=0, scale=None, scaleVel=1):
        return part

class ExplosionEmitter(ParticleEmitter):
    def __init__(self, parent,size):
        super().__init__(parent,0, 0)
        self.radius = size
        self.active= False
        self.emitCount = math.floor((10*size/60)**2)
        self.emitCooldownMax=0

    def getParticle(self):
        if ((not self.active or self.emitCooldown > 0)):
            return None
        pos = self.getPosition()
        trans = pygame.math.Vector2(self.radius*(0.01+0.9*random.random()), 0).rotate(random.random() * 360);
        pos += trans
        part = View.Particles.ExplosionParticle(pos.x, pos.y,self.parent.velocity+10*trans)
        return part