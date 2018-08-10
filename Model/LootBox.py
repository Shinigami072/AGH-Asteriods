import random
import math
import Files
import Sound
from Model.Ship import Ship
from Model.GameObj import GameObj

class LootBox(GameObj):

    def __init__(self,x,y,game,type="hp"):
        super().__init__(x,y)
        self.rotation=360*random.random()
        self.rotVel=(5+15*random.random())*random.choice([1,-1])
        self.scale=20
        self.mass=90000
        self.setModel(Files.Models["box_bg"])
        self.hit=False
        self.harmful=False
        self.game=game
        self.setType(type)
        self.bias=19

    def setType(self,type):
        self.type=type
        self.typeModel=Files.Models["lootbox_"+type]

    def getCollider(self):
        return 19

    def isInteractable(self, a):
        return not isinstance(a,Ship)
    def crack(self,game):
        Sound.playSound("pickup")
        self.alive=False
        if(self.type =="hp"):
            game.messages.append("Picked up Repair Kit")
            game.hp+=1
        elif(self.type =="score1"):
            game.messages.append("Picked up Small Mineral Bundle")
            game.score+=100
        elif (self.type == "score2"):
            game.messages.append("Picked up Medium Mineral Bundle")
            game.score += 150
        elif (self.type == "score3"):
            game.messages.append("Picked up Large Mineral Bundle")
            game.score += 200

        elif (self.type == "invin"):
            game.messages.append("Picked up Temporary Shield")
            game.ship.inV += 5

    def update(self,delta):
        if(self.hit):
            self.crack(self.game)

        dist =self.game.ship.position-self.position
        if(dist).length()<100 and dist.length()>5 :
            self.velocity+=dist.normalize()*2500*delta
            if(dist.length()<50):
                self.velocity=dist*50

        self.updateMotion(delta)

    def onCollide(self,ship):
        if(isinstance(ship,Ship)):
            self.hit=True
