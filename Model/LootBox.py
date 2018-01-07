import random
import math
import Files
import Sound
from Model.Ship import Ship
from Model.GameObj import GameObj

class LootBox(GameObj):

    def __init__(self,x,y,game):
        super().__init__(x,y)
        self.rotation=360*random.random()
        self.rotVel=(5+15*random.random())*random.choice([1,-1])
        self.scale=20#
        self.mass=90000
        self.setModel(Files.Models["box_bg"])
        self.hit=False
        self.typeModel=Files.Models["lootbox_hp"]
        self.harmful=False
        self.game=game

    def getCollider(self):
        return 19

    def isInteractable(self, a):
        return not isinstance(a,Ship)
    def crack(self,game):
        Sound.playSound("pickup")
        self.alive=False
        game.hp+=1

    def update(self,delta):
        if(self.hit):
            self.crack(self.game)

        dist =self.game.ship.position-self.position
        if(dist).length()<100 and dist.length()>5 :
            print("HERE")
            self.velocity+=dist.normalize()*2500*delta
            if(dist.length()<50):
                self.velocity=dist*50
        self.updateMotion(delta)
    def onCollide(self,ship):
        if(isinstance(ship,Ship)):
            self.hit=True
