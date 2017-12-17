import pygame
import random
#m - kg
#V - m/s
class Particle:
    def __init__(self,x,y):
        self.position =pygame.math.Vector2(x,y)
        self.velocity =pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.rotation = 0
        self.life =10
        self.mass=0.1;
        self.alive = True


    def updateMotion(self,delta):
        self.velocity += self.acceleration*delta;
        self.position += self.velocity*delta;
        if self.life >0:
            self.life-=delta
        else:
            self.alive=False
        pass

class ParticleThruster(Particle):
    def __init__(self,x,y,rotation,scale):
        super().__init__(x,y)
        self.velocity =pygame.math.Vector2(200*(0.5+(random.random()*0.5)),5*2*(random.random()-0.5))
        self.velocity =-self.velocity.rotate(rotation)
        self.life =0.2+(0.5+0.4*random.random())*scale;

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
