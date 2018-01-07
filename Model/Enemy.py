#TODO: menu
#TODO: ememies

#TODO: poziomy trudności
#TODO: endgame

#TODO: Sounds

#TODO: shipChoice
#TODO: load models
#TODO: graphics update
import Sound
from Model.GameObj import GameObj
from pygame.math import Vector2
import Model.Bullet
import Model.Asteroid
import random
import math
import Files
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
        self.searchangle=0
        self.targetReached=False


    def chaseTaget(self,body,delta):
        # KOD FIZYCZNY #
        # ZAPYTAJ RAFAłA jak działa
        # nikt nie jest pewien dlaczego działa

        dis = (Vector2(self.target) - body.position)
        dist = dis.length()

        angle = dis.angle_to(Vector2(1, 0).rotate(body.rotation))
        self.inputRotation = body.rotation - angle

        deltasq = math.sqrt(2*(body.velocity.x)**2 + 4*body.maxAccel*math.fabs(dis.x))
        t1 = (-2*math.fabs(body.velocity.x)+deltasq)/(2*body.maxAccel)
        t2=math.fabs(body.velocity.x)/body.maxAccel

        if (t1-delta > 0):
            if(dis.x >0):
                self.inputVector.x = 1
            else:
                self.inputVector.x = -1
        elif (t2-delta > 0):
            if (dis.x > 0):
                self.inputVector.x = -1
            else:
                self.inputVector.x = 1
        else:
            self.inputVector.x = 0
            body.velocity.x = 0

        deltasq = math.sqrt(2 * (body.velocity.y) ** 2 + 4 * body.maxAccel * math.fabs(dis.y))
        t1 = (-2 * math.fabs(body.velocity.y) + deltasq) / (2 * body.maxAccel)
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
        if(self.inputVector.x ==0 and self.inputVector.y ==0):
            self.targetReached=True




    def update(self,delta,game,body):
        if self.target == (-1, -1):
            self.target = (random.random() * game.WIDTH, random.random() * game.HEIGHT)

        dis = (game.ship.position - body.position)
        dist = dis.length()
        angle = dis.angle_to(Vector2(1, 0).rotate(body.rotation))
        #self.target = (body.position.x + 100, body.position.y)
        self.searchtimer += delta

        self.targetReached = False
        self.chaseTaget(body, delta)

        #if not self.chase:
        #    self.chaseTaget(body,delta)
        #    self.chase=True
        if( self.searchArea is None):
            print("setting")
            self.searchArea = body.position

        if(self.mode == "IDLE"):
            if(self.searchtimer >= AI.SEARCHTIMER_MAX  or self.targetReached):
                self.searchtimer=0
                self.target = (random.random()*game.WIDTH, random.random()*game.HEIGHT)
            if(dist<500):
                self.searchArea = (body.position.x,body.position.y)
                self.mode= "SEARCH"
                self.searchtimer=0

        elif(self.mode =="SEARCH"):
            if math.fabs(angle)<=10 and dist <500:
                self.mode="DESTROY"
                self.searchtimer=0
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
            if math.fabs(angle) <= 30:
                self.searchtimer=0

                self.target = (game.ship.position.x,game.ship.position.y)-dis.normalize()*300
                self.inputRotation= body.rotation - angle
            elif (self.searchtimer >= AI.SEARCHTIMER_MAX or self.targetReached):
                self.mode = "SEARCH"
                self.searchArea = (body.position.x,body.position.y)
                self.searchtimer=0



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

    def getCollider(self):
        return 50
    def isCollideable(self,a):
        return not isinstance(a,Model.Asteroid.Asteroid)

    def destroy(self,game,i):
        Sound.playSound("explode")
        self.particleEmitters["explode"].active=True
        self.alive=False
        game.score +=150

    def isInteractable(self, a):
        return False

    def update(self,delta):
        if(self.velocity.length()>self.maxAccel*1.5):
            self.velocity.scale_to_length(self.maxAccel*1.5)
        #self.cooldown -= delta
        #dir = (self.game.ship.position+self.game.ship.velocity*dist/1000 - self.position)
        #self.rotation = -self.velocity.angle_to(Vector2(1,0))
        #self.velocity = Vector2(100, 0).rotate(self.rotation)  # 100*dir

        #self.velocity= 300*self.dir + 300*math.sin(self.cooldown/(self.maxCooldown/2)*2*math.pi)*self.dir.rotate(90)

        #if (self.cooldown <= 0):
        #   Sound.playSound("laser0")
        #    self.dir = self.dir.rotate(90 *(-1+2*random.random()))
        #    self.cooldown = self.maxCooldown
        #    b = Model.Bullet.Bullet(self.position.x, self.position.y, 1000, -dir.rotate(10/(self.game.score/100+1)*(-1+2*random.random())).angle_to(Vector2(1,0)), self)
        #    self.game.gameObjects.append(b)
        self.AI.update(delta,self.game,self)

        self.rotVel = 4*720*self.getQuickestRot(self.AI.inputRotation)/360#Controller.inputVector.x*self.maxRotation*delta
        #self.acceleration =Vector2(0,0)
        #if self.AI.inputVector.y > 0 or self.AI.inputVector.y <0:
         #   self.acceleration += self.maxAccel*self.AI.inputVector.y#*Vector2(1, 0).rotate(self.rotation)

        #if self.AI.inputVector.x > 0 or self.AI.inputVector.x < 0:

        self.acceleration = self.maxAccel* self.AI.inputVector# * Vector2(0, 1).rotate(self.rotation)

        #thrustconrol
        thrustc = self.AI.inputVector.rotate(self.rotation+90)
        self.setGroupActive("thrusters", False,True)
        self.setGroupActive("thrusterUP", thrustc.y>0.2)
        self.setGroupActive("thrusterDOWN", thrustc.y<-0.2)
        self.setGroupActive("thrusterLEFT", thrustc.x < -0.2)
        self.setGroupActive("thrusterRIGHT", thrustc.x>0.2)
        self.setGroupActive("thrusterRotLeft", self.rotVel>15)
        self.setGroupActive("thrusterRotRight", self.rotVel<-15)



        self.updateMotion(delta)
