import pygame
import math
import random
import Model.Asteroid as Asteroid
import Model.Bullet as Bullet
import Model.GameObj as GameObj
import Model.Ship as Ship
from Model.Enemy import Enemy
import View.Particles as Particles
import Files
import Controller
from Model.LootBox import LootBox
FPS = 60
#HEIGHT_P = 720
#WIDTH_P = 1280
HEIGHT_P = 1080
WIDTH_P = 1920

BLACK = (0,0,0)
WHITE = (255,255,255)
DEBUG_BLUE = (0,220,220)
DEBUG_PURPLE = (220,0,220)
DEBUG_YELLOW = (220,220,0)



#
#klasa rozdzielająca gamespace i screenspace
#zajmuje się całóścią renderowania

class Renderer:
    fonts ={}
    def __init__(self,width,height):
        global WIDTH_P
        global HEIGHT_P

        self.M_TO_P = max((width)/WIDTH_P,(height)/HEIGHT_P)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_P, HEIGHT_P))
        if(len(Renderer.fonts) ==0):
            Renderer.fonts = {"default":pygame.font.SysFont(pygame.font.get_default_font(), 72)}
        self.font = Renderer.fonts["default"]
        self.clock = pygame.time.Clock()
        self.DEBUG = False

    def render(self,game,delta):
        pass

    def getMP(self,m):
        return m / self.M_TO_P

    def getMPPos(self,m):
        return self.getMP(m - 20)


class VectorRenderer(Renderer):

    def __init__(self,width,height):
        super().__init__(width,height)
        self.M_TO_P = max((width-80)/WIDTH_P,(height-80)/HEIGHT_P)
        self.shipTimer = 0.2
        self.lootTimer = 0.2
        self.particles = []
        self.particleCount=0;

    def renderAsteroid(self,astroid):
        #pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(astroid.position.x)),math.floor(getMP(astroid.position.y))),math.floor(getMP(Asteroid.ASTEROID_SIZES[astroid.size]["size"])));
        rot = astroid.rotation
        scale = self.getMP(Asteroid.ASTEROID_SIZES[astroid.size]["size"])
        shape = astroid.model.getModel(self.getMP(astroid.position.x),self.getMP(astroid.position.y),rot=rot,scale=scale)
        pygame.draw.polygon(self.screen,WHITE,shape)


    def renderVelocity(self,object):
        pygame.draw.aaline(self.screen,DEBUG_BLUE,
                           (self.getMP(object.position.x),self.getMP(object.position.y)),
                           (self.getMP(object.position.x+object.velocity.x),self.getMP(object.position.y+object.velocity.y)))
    def renderRotation(self,object):
        test = pygame.math.Vector2(100, 0);
        pygame.draw.aaline(self.screen, DEBUG_PURPLE,
                           (self.getMP(object.position.x + (test.rotate(object.rotation) / 2).x),
                            self.getMP(object.position.y + (test.rotate(object.rotation) / 2).y)),
                           (self.getMP(object.position.x + test.rotate(object.rotation).x),
                            self.getMP(object.position.y + test.rotate(object.rotation).y)))
       # self.screen.blit(
       #         self.font.render("rot:{:3.1f}' rotV{:3.1f}'/s ".format(object.rotation, object.rotVel), True,
       #                          DEBUG_BLUE), (self.getMP(object.position.x), self.getMP(object.position.y) - 35))

    def renderCollider(self,object):
        rad = object.getCollider()
        if rad is None:
            return

        pygame.draw.circle(self.screen,DEBUG_BLUE,(math.floor(self.getMP(object.position.x)),math.floor(self.getMP(object.position.y))),math.floor(self.getMP(rad)),min(2,math.floor(self.getMP(rad))));

    def renderShipAt(self,x,y,size,rotation):
        m = Files.Models["Classic"]

        pygame.draw.polygon(self.screen,WHITE, m.getModel(x,y,scale=size,rot=rotation))

        #print((80 * math.cos(math.radians(0)), 80 * math.sin(math.radians(0))),
        #      (40 * math.cos(math.radians(120)), 40 * math.sin(math.radians(120))),
        #      (0, 0),
        #      (40 * math.cos(math.radians(-120)), 40 * math.sin(math.radians(-120))))

        #pygame.draw.polygon(self.screen,WHITE,
        #                    ((x+self.getMP(size*80)*math.cos(math.radians(rotation)),y+self.getMP(size*80)*math.sin(math.radians(rotation))),
        #                     (x+self.getMP(size*40)*math.cos(math.radians(rotation+120)),y+self.getMP(size*40)*math.sin(math.radians(rotation+120))),
        #                     (x,y),
        #                     (x+self.getMP(size*40)*math.cos(math.radians(rotation-120)),y+self.getMP(size*40)*math.sin(math.radians(rotation-120)))))

    def renderShip(self,ship,width,height):
        rot = ship.rotation
        scale = self.getMP(ship.scale*ship.modelScale)
        shape = ship.model.getModel(self.getMP(ship.position.x),self.getMP(ship.position.y),rot=rot,scale=scale)
        if(self.shipTimer<0.2):
            pygame.draw.polygon(self.screen,WHITE,shape)

        #self.renderShipAt(self.getMP(ship.position.x)        ,self.getMP(ship.position.y)          ,ship.size,ship.rotation)
        #self.renderShipAt(self.getMP(ship.position.x+width)  ,self.getMP(ship.position.y)          ,ship.size,ship.rotation)
        #self.renderShipAt(self.getMP(ship.position.x-width)  ,self.getMP(ship.position.y)          ,ship.size,ship.rotation)
        #self.renderShipAt(self.getMP(ship.position.x)        ,self.getMP(ship.position.y+height)   ,ship.size,ship.rotation)
        #self.renderShipAt(self.getMP(ship.position.x)        ,self.getMP(ship.position.y-height)   ,ship.size,ship.rotation)
        if (self.DEBUG):
            test = pygame.math.Vector2(100,0);
            pygame.draw.aaline(self.screen, DEBUG_PURPLE,
                               (self.getMP(ship.position.x + (test.rotate(ship.rotation)/2).x),
                                self.getMP(ship.position.y+  (test.rotate(ship.rotation)/2).y)),
                               (self.getMP(ship.position.x + test.rotate(ship.rotation).x),
                                self.getMP(ship.position.y + test.rotate(ship.rotation).y)))
            pygame.draw.aaline(self.screen, DEBUG_YELLOW,
                               (self.getMP(ship.position.x + (test.rotate(Controller.inputRotation) / 2).x),
                                self.getMP(ship.position.y + (test.rotate(Controller.inputRotation) / 2).y)),
                               (self.getMP(ship.position.x + test.rotate(Controller.inputRotation).x),
                                self.getMP(ship.position.y + test.rotate(Controller.inputRotation).y)))
            test=Controller.inputVector
            pygame.draw.aaline(self.screen, DEBUG_YELLOW,
                               (self.getMP(ship.position.x), self.getMP(ship.position.y)),
                               (self.getMP(ship.position.x + test.rotate(ship.rotation+90).x*100),
                                self.getMP(ship.position.y + test.rotate(ship.rotation+90).y*100)))

        return

    def renderBullet(self,bullet):
        pygame.draw.circle(self.screen,WHITE,(math.floor(self.getMP(bullet.position.x)),math.floor(self.getMP(bullet.position.y))),math.floor(self.getMP(5)));

    def renderEnemy(self, enemy):
        rot= enemy.rotation
        scale=self.getMP(enemy.getCollider())
        shape = enemy.model.getModel(self.getMP(enemy.position.x), self.getMP(enemy.position.y), rot=rot,
                                       scale=scale)
        pygame.draw.polygon(self.screen, WHITE, shape)
        if (self.DEBUG):
            c = WHITE
            if(enemy.AI.mode == "IDLE"):
                c= DEBUG_PURPLE
            elif (enemy.AI.mode == "SEARCH"):
                c = DEBUG_BLUE
            elif (enemy.AI.mode == "DESTROY"):
                c = DEBUG_YELLOW

            pygame.draw.circle(self.screen, c,
                              (math.floor(self.getMP(enemy.position.x)), math.floor(self.getMP(enemy.position.y))),
                               math.floor(self.getMP(90)),12);

            pygame.draw.aaline(self.screen,DEBUG_BLUE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x )+390* math.cos(math.radians(enemy.rotation+10)), self.getMP(enemy.position.y)+ 390*math.sin(math.radians(enemy.rotation+10)))
                               )
            pygame.draw.aaline(self.screen, DEBUG_BLUE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + 390 * math.cos(math.radians(enemy.rotation - 10)),
                                self.getMP(enemy.position.y) + 390 * math.sin(math.radians(enemy.rotation - 10)))
                               )

            pygame.draw.circle(self.screen, c,
                               (math.floor(self.getMP(enemy.AI.target[0])), math.floor(self.getMP(enemy.AI.target[1]))),
                               math.floor(self.getMP(20)), 12);

    def renderLootBox(self,lootbox):
        rot = lootbox.rotation
        scale = self.getMP(lootbox.scale)
        shape = lootbox.model.getModel(self.getMP(lootbox.position.x),self.getMP(lootbox.position.y),rot=rot,scale=scale)

        pygame.draw.polygon(self.screen,WHITE,shape)

        shape2 = lootbox.typeModel.getModel(self.getMP(lootbox.position.x),self.getMP(lootbox.position.y),rot=rot,scale=scale)
        pygame.draw.polygon(self.screen,(90,90,90),shape2)

        wh = pygame.math.Vector3(WHITE)
        bl = pygame.math.Vector3(BLACK)

        if(self.lootTimer<1) and self.lootTimer>=0:
            lootscale = (1-(self.lootTimer)/1)
            rad=200*lootscale

            pygame.draw.circle(self.screen,(bl.lerp(wh,1-lootscale)),(math.floor(self.getMP(lootbox.position.x)),math.floor(self.getMP(lootbox.position.y))),math.floor(rad),6 if rad>6 else 0);



    def renderParticle(self,particle):
        wh =pygame.math.Vector3(WHITE)
        bl = pygame.math.Vector3(BLACK)

        pygame.draw.circle(self.screen,(bl.lerp(wh,particle.getlifeP())),(math.floor(self.getMP(particle.position.x)),math.floor(self.getMP(particle.position.y))),math.floor(self.getMP(5*particle.scale)));
    def handleParticleEmitter(self,particleEmitter,delta):
        particleEmitter.update(delta)
        if (self.DEBUG):
            pos =particleEmitter.getPosition()
            pygame.draw.circle(self.screen,DEBUG_PURPLE,(math.floor(self.getMP(pos.x)),math.floor(self.getMP(pos.y))),2)
        if(particleEmitter.emitCooldown<=0 and self.particleCount<1000 and particleEmitter.active):
            for i in range(particleEmitter.emitCount):
                if(self.particleCount<1000):
                    p = particleEmitter.getParticle()
                    if not p is None:
                        self.particles.append(p)

    def render(self,game,delta):
        if(game.ship.inV>0 and self.shipTimer<=0):
            self.shipTimer=0.3
        if(game.ship.inV>0):
            self.shipTimer-=delta
        else:
            self.shipTimer=0;

        if (self.lootTimer > 0):
            self.lootTimer -= delta
        else:
            self.lootTimer = 7.5;

        self.particleCount = len(self.particles)
        for particle in self.particles:
            if (not Controller.inputButtons["pause"]):
                particle.updateMotion(delta)
            self.renderParticle(particle)
            if(not particle.alive):
                self.particles.remove(particle)


        if(self.DEBUG):
            #print("FPS:{:3.1f} {:3.1f}ms".format(1/delta,delta*1000))
            self.screen.blit(self.font.render("FPS:{:3.1f} {:3.1f}ms".format(1/delta,delta*1000),True,DEBUG_BLUE),(0,30))

        self.screen.blit(self.font.render("SCORE:{:3.0f}".format(game.score), True,WHITE),(0, 0))
        self.screen.blit(self.font.render("HP:{:3.0f}".format(game.hp), True,WHITE),(0, HEIGHT_P-72))

        for i in range(game.hp):
            self.renderShipAt(20+i*40, HEIGHT_P-72-20,20,-90)
        pygame.draw.circle(self.screen,WHITE,(0,0),10)
        for gameObject in game.gameObjects:
            if (isinstance(gameObject, Asteroid.Asteroid)):
                self.renderAsteroid(gameObject)
            if (isinstance(gameObject, Ship.Ship) and self.shipTimer<=0.5):
                self.renderShip(gameObject,game.WIDTH,game.HEIGHT)
            if (isinstance(gameObject, Bullet.Bullet)):
                self.renderBullet(gameObject)
            if (isinstance(gameObject, Enemy)):
                self.renderEnemy(gameObject)
            if (isinstance(gameObject, LootBox)):
                self.renderLootBox(gameObject)
            if(self.DEBUG):
                    if(isinstance(gameObject,GameObj.GameObj)):
                        self.renderVelocity(gameObject)
                        self.renderCollider(gameObject)
                        if(not isinstance(gameObject, Ship.Ship)):
                            self.renderRotation(gameObject)
            if(not Controller.inputButtons["pause"]):
                for particleEmitter in gameObject.particleEmitters:
                    self.handleParticleEmitter(gameObject.particleEmitters[particleEmitter], delta)

        #pygame.display.flip()

