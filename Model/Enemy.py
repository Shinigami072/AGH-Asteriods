
import Sound
from Model.GameObj import GameObj
from pygame.math import Vector2
import Model.Bullet
import Model.Asteroid
import random
import math
import Files
from Model.LootBox import LootBox
class AI:
    MODES = ["IDLE","SEARCH","DESTROY"]
    SEARCHTIMER_MAX=10
    def __init__(self,mode):
        self.mode="IDLE"
        self.inputVector = Vector2(0,0)
        self.inputRotation=0

        self.searchtimer = 0
        self.timer2 = 0

        self.target = (-1,-1)
        self.searchArea = None
        self.searchangle=10
        self.searchdist=500
        self.targetReached=False

        self.shotangle =10


    def chaseTaget(self,body,delta):

        # KOD FIZYCZNY #
        # poniższy kod jest implementacja równań które wyprowadził rafał

        dis = (Vector2(self.target) - body.position)
        dist = dis.length()

        angle = dis.angle_to(Vector2(1, 0).rotate(body.rotation))
        self.inputRotation = body.rotation - angle

        deltasq = math.sqrt(2*(body.velocity.x) ** 2 + 4*body.maxAccel * math.fabs(dis.x))
        t1 = (-2*math.fabs(body.velocity.x) + deltasq) / (2*body.maxAccel)
        t2 = math.fabs(body.velocity.x) / body.maxAccel

        if (t1 - delta > 0):
            if (dis.x > 0):
                self.inputVector.x = 1
            else:
                self.inputVector.x = -1
        elif (t2 - delta > 0):
            if (dis.x > 0):
                self.inputVector.x = -1
            else:
                self.inputVector.x = 1
        else:
            self.inputVector.x = 0
            body.velocity.x = 0

        deltasq = math.sqrt(2*(body.velocity.y) ** 2 +4* body.maxAccel * math.fabs(dis.y))
        t1 = (-2*math.fabs(body.velocity.y) + deltasq) / (2* body.maxAccel)
        t2 = math.fabs(body.velocity.y) / body.maxAccel

        if (t1 - delta > 0):
            if (dis.y > 0):
                self.inputVector.y = 1
            else:
                self.inputVector.y = -1
        elif (t2 - delta > 0):
            if (dis.y > 0):
                self.inputVector.y = -1
            else:
                self.inputVector.y = 1
        else:
            self.inputVector.y = 0
            body.velocity.y = 0
        ###
        #koniec kodu fizycznego

        if (self.inputVector.x == 0 and self.inputVector.y == 0):
            self.targetReached = True




    def update(self,delta,game,body):
        if self.target == (-1, -1):
            self.target = (random.random() * game.WIDTH, random.random() * game.HEIGHT)

        dis = (game.ship.position - body.position)
        dist = dis.length()
        angle = dis.angle_to(Vector2(1, 0).rotate(body.rotation))

        self.searchtimer += delta
        self.targetReached = False
        self.chaseTaget(body, delta)

        self.shotangle = 50/(game.score/100+1)
        if(self.shotangle < 0.3):
         self.shotangle = 0

        if game.ship.dead:
            self.mode ="IDLE"

        if( self.searchArea is None):
            print("setting")
            self.searchArea = body.position

        if(self.mode == "IDLE"):
            self.searchdist = 500*math.sqrt(game.level())
            if(self.searchtimer >= AI.SEARCHTIMER_MAX  or self.targetReached):
                self.searchtimer=0
                self.target = (random.random()*game.WIDTH, random.random()*game.HEIGHT)
            if(dist<self.searchdist):
                self.searchArea = (body.position.x,body.position.y)
                self.mode= "SEARCH"
                self.searchtimer=0

        elif(self.mode =="SEARCH"):
            self.searchangle=10*math.sqrt(game.level())
            self.searchdist = 500*math.sqrt(game.level())
            if math.fabs(angle)<=self.searchangle and dist <self.searchdist:
                self.mode="DESTROY"
                game.addMsg("Alien weapons charging")
                Sound.playSound("change")
                self.searchtimer=0
                self.timer2=3
            else:
                self.timer2-=delta
                if(self.timer2<0 or self.targetReached):
                    self.searchangle+= random.choice([1,-1])*60*(random.random()*0.3+0.7)
                    rad = 200*(random.random()* 0.3 + 0.7)
                    self.target = (self.searchArea[0]+math.cos(self.searchangle)*rad, self.searchArea[1]+math.sin(self.searchangle)*rad)
                    self.timer2=2

            if(self.searchtimer >= AI.SEARCHTIMER_MAX):
                self.mode="IDLE"

        elif(self.mode =="DESTROY"):
            self.searchangle=30*math.sqrt(game.level())
            self.searchdist = 3000
            if math.fabs(angle) <= self.searchangle:
                self.searchtimer=0
                self.target = (game.ship.position.x,game.ship.position.y)-dis.normalize()*300
                self.inputRotation= body.rotation - angle
                self.timer2-=delta
                if(self.timer2<0):
                    self.timer2=2/game.level()
                    Sound.playSound("laser")
                    b = Model.Bullet.Bullet(body.position.x, body.position.y, 1000, -dis.rotate(
                        self.shotangle*(-1 + 2 * random.random())).angle_to(Vector2(1, 0)), body)
                    game.gameObjects.append(b)

            elif (self.searchtimer >= AI.SEARCHTIMER_MAX or self.targetReached):
                self.mode = "SEARCH"
                game.addMsg("Alien tracking scrambled")
                Sound.playSound("click")
                self.searchArea = (body.position.x,body.position.y)
                self.searchtimer=0
            else:
                self.timer2=3



class Enemy(GameObj):

    def __init__(self,x,y,game):
        super().__init__(x,y)
        self.game=game
        self.AI=AI("IDLE")
        self.hit = False
        self.setModel(Files.Models["enemy0"])
        self.setGroupActive("thrusterUP",True)
        self.thrustScale=1;
        self.scale=50
        self.maxAccel=200
        game.addMsg("Alien presence detected")

    def getCollider(self):
        return 50
    def isCollideable(self,a):
        return not isinstance(a,Model.Asteroid.Asteroid)

    def destroy(self,game,i):
        Sound.playSound("explode")
        self.particleEmitters["explode"].active=True
        self.alive=False
        game.addMsg("Alien presence vanished")
        if(game.ship.dead):
            game.addMsg("from the Grave +100")
            game.score+=100

        game.gameObjects.append(Model.LootBox.LootBox(
            random.choice([-1,1])*random.random()*10+self.position.x,
            random.choice([-1, 1]) * random.random() * 10 + self.position.y, game
            , random.choice(["score1"]*10+["invin"]+["score2"]*4+["score3"])
        ))


    def isInteractable(self, a):
        return False

    def update(self,delta):
        if(self.velocity.length()>self.maxAccel*1.5): #limitowanie prędkości
            self.velocity.scale_to_length(self.maxAccel*1.5)

        self.AI.update(delta,self.game,self)

        #zarzadzenie rcuhem przez AI
        self.rotVel = 4*self.getQuickestRot(self.AI.inputRotation)
        self.acceleration = self.maxAccel* self.AI.inputVector

        #thrustconrol - zarzadzenie emiterami cząsteczek
        thrustc = self.AI.inputVector.rotate(self.rotation+90)
        self.setGroupActive("thrusters", False,True)
        self.setGroupActive("thrusterUP", thrustc.y>0.2)
        self.setGroupActive("thrusterDOWN", thrustc.y<-0.2)
        self.setGroupActive("thrusterLEFT", thrustc.x < -0.2)
        self.setGroupActive("thrusterRIGHT", thrustc.x>0.2)
        self.setGroupActive("thrusterRotLeft", self.rotVel>15)
        self.setGroupActive("thrusterRotRight", self.rotVel<-15)


        self.updateMotion(delta)
