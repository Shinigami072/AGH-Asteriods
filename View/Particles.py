import pygame
import random
import Model.GameObj
#m - kg
#V - m/s

#wszyskie cząsteczki w grze - ich ruch i inne dane
class Particle:
    def __init__(self,x,y,maxlife=10):
        self.position =pygame.math.Vector2(x,y)
        self.velocity =pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.rotation = 0
        self.scale=1
        self.maxlife = maxlife
        self.life =self.maxlife
        self.mass=0.1;
        self.alive = True

    def getlifeP(self):
        life = self.life/self.maxlife;
        if(life<0):
            return 0
        return life
    def updateMotion(self,delta):
        self.velocity += self.acceleration*delta;
        self.position += self.velocity*delta;
        if self.life >0:
            self.life-=delta
        else:
            self.alive=False
        pass



class ExplosionParticle(Particle):
    def __init__(self, x, y,velocity):
        super().__init__(x,y,maxlife=2*(random.random()*0.7+0.3))
        self.velocity=velocity
        self.scale=random.random()+0.3


    def updateMotion(self,delta):
        super().updateMotion(delta)
        self.scale=self.getlifeP()

class ParticleThruster(Particle):
    def __init__(self,x,y,ship,rotation=0,scale=None,scaleVel=1):
        if (not scale):
            scale = ship.thrustScale

        life=0.2+(0.5+0.4*random.random())*scale
        super().__init__(x,y,maxlife=life)
        self.scale=0.5+0.9*random.random()
        self.velocity =pygame.math.Vector2(200*scaleVel*(0.5+(random.random()*0.5)),5*2*(random.random()-0.5))
        self.velocity =-self.velocity.rotate(ship.rotation+rotation)
        self.velocity += ship.velocity;

    def updateMotion(self,delta):
        self.velocity += self.acceleration*delta;
        self.position += self.velocity*delta;
        self.velocity.x += 12*(random.random()-0.5)
        self.velocity.y += 12*(random.random()-0.5)
        self.velocity *= 1-delta*0.9

        if self.life >0:
            self.life-=delta
        else:
            self.alive=False
        pass
