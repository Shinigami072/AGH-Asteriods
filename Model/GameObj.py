import pygame
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
            if None is self.getCollider() or a.getCollider() is None:
                return False
            diff = self.position-a.position
            dist = (self.getCollider()+a.getCollider())**2
            collided = diff.length_squared()<=dist
            return collided

    def update(self,delta):
            self.updateMotion(delta)