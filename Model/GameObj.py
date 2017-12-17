import pygame
import View.Particles
import random
#m - kg
#V - m/s
class GameObj:
    def __init__(self,x,y):
        self.position =pygame.math.Vector2(x,y)
        self.velocity =pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.rotation = 0
        self.maxAccel=50;
        self.mass=1;
        self.alive = True


    def updateMotion(self,delta):
        self.velocity += self.acceleration*delta;
        self.position += self.velocity*delta;
        pass

    def getCollider(self):
        return None
    def onCollide(self,a):
        pass
    def render(self,screen,delta,game):
        pass
    def isCollideable(self,a):
        return True
    def collide(self,a):
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

        a.onCollide(self)
        self.onCollide(a)

    def checkCollision(self, a):
            if None is self.getCollider() or a.getCollider() is None or not self.alive or not a.alive:
                return False
            diff = self.position-a.position
            dist = (self.getCollider()+a.getCollider())**2
            collided = diff.length_squared()<=dist
            return collided

    def update(self,delta):
            self.updateMotion(delta)
class ParticleEmiter(GameObj):
    def __init__(self,x,y):
        self.position =pygame.math.Vector2(x,y)
        self.velocity =pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.rotation = 0
        self.maxAccel=50;
        self.mass=1;
        self.alive = True
        self.emitCount =100
        self.emitCooldown=0.01;
        self.emitCooldownMax=10;

    def getParticle(self):
        #p = View.Particles.ParticleThruster(self.position.x,self.position.y,random.random()*360,random.random()*10)
        p = View.Particles.Particle(self.position.x,self.position.y)
        p.velocity += pygame.math.Vector2(0,random.random()*150+50).rotate(random.random()*360)
        p.position += pygame.math.Vector2(0,400).rotate(random.random()*360)
        return p

    def isCollideable(self,a):
        return False

    def checkCollision(self, a):
        return False

    def update(self,delta):
            if(self.emitCooldown>0):
                self.emitCooldown-=delta
            else:
                self.emitCooldown=self.emitCooldownMax

            self.updateMotion(delta)