import pygame
import math
import Controller
import Files
import Sound
from Model.GameObj import GameObj as GameObj


class Ship(GameObj):
    def __init__(self,x,y):
        super().__init__(x,y);
        self.rotation = 0
        self.maxRotation =3000;
        self.maxAccel=250;
        self.scale = 0.5
        self.modelScale=80
        self.coolDown = 0;
        self.maxColdown =0.2;
        self.mass = 20000
        self.dead=False
        self.thrusting = False
        self.maneuver = False
        self.maneuverSide = False
        self.thrustDir =False
        self.thrustScale = 0
        self.inV = 3
        self.setModel(Files.ModelGroups["ship"].getRandomModel())

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

    def setDead(self,d):
        print(d)
        self.dead = d
        self.particleEmitters["explode"].active = d
        if d:
         Sound.playSound("explode")
        if not d:
            self.setModel(Files.ModelGroups["ship"].getRandomModel())
    def onCollide(self,a):
        if(self.inV<=0 and a.harmful):
            self.setDead(True)

        print("Ship Cosllison Detected",type(a))

    def update(self,delta):
        if(self.coolDown>0):
            self.coolDown-=delta
        if(self.coolDown<0):
            self.coolDown=0;
        if (self.inV > 0):
            self.inV -= delta
        if (self.inV < 0):
            self.inV = 0;


        self.rotVel = self.maxRotation*self.getQuickestRot(Controller.inputRotation)/360#Controller.inputVector.x*self.maxRotation*delta
        self.maneuver = Controller.inputVector.x > 0 or Controller.inputVector.x < 0
        self.maneuverSide = Controller.inputVector.x > 0

        self.acceleration.x =0
        self.acceleration.y =0

        if Controller.inputVector.x > 0 or Controller.inputVector.x <0:
            self.acceleration += self.maxAccel/4*3*Controller.inputVector.x*pygame.math.Vector2(0, 1).rotate(self.rotation)

        self.setGroupActive("thrusters", False,True)

        self.setGroupActive("thrusterRotLeft", self.getQuickestRot(Controller.inputRotation) > 10)
        self.setGroupActive("thrusterRotRight", self.getQuickestRot(Controller.inputRotation) < -10)


        self.setGroupActive("thrusterLEFT", Controller.inputVector.x > 0)
        self.setGroupActive("thrusterRIGHT", Controller.inputVector.x < 0)

        self.setGroupActive("thrusterUP", Controller.inputVector.y > 0)
        self.setGroupActive("thrusterDOWN", Controller.inputVector.y < 0)
        if Controller.inputVector.y > 0 or Controller.inputVector.y <0:
            self.thrustScale = math.fabs(Controller.inputVector.y)
            self.acceleration += self.maxAccel*Controller.inputVector.y*pygame.math.Vector2(1, 0).rotate(self.rotation)
            if( not self.thrustDir):
                self.acceleration/=2
        else:
            self.thrustScale = 0

        GameObj.updateMotion(self,delta)

