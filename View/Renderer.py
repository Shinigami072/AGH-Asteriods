import pygame
import math
import random
import Model.Asteroid as Asteroid
import Model.Bullet as Bullet
import Model.GameObj as GameObj
import Model.Ship as Ship
import View.Particles as Particles

FPS = 60
#HEIGHT_P = 720
#WIDTH_P = 1280
HEIGHT_P = 1080
WIDTH_P = 1920
M_TO_P = 10

BLACK = (0,0,0)
WHITE = (255,255,255)
DEBUG_BLUE = (0,220,220)
DEBUG_PURPLE = (220,0,220)

DEBUG = True

def getMP(m):
    return m/M_TO_P
def getMPPos(m):
    return getMP(m-20)

class Renderer:

    def __init__(self,game):
        global M_TO_P
        global WIDTH_P
        global HEIGHT_P

        M_TO_P = max((game.WIDTH-80)/WIDTH_P,(game.HEIGHT-80)/HEIGHT_P)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_P, HEIGHT_P))
        self.clock = pygame.time.Clock()

    def render(self,game):
        pass

ASTEROID_SHAPES = {
        "XLARGE": (
            [(0, 0.6), (0.9, 1), (1, 0.6),(0.7, 0.65), (0.7, 0.3),(1.1,0), (1.1,-0.1),(0.4,-0.5), (0.6,-0.9), (-0.5,-1),(-1,-0.1),(-0.7,0.3),(-0.3,0.7)],
            [(0, -1), (0.8, -0.7), (0.9, 0), (1, 0.5), (0.5, 1), (-0.8, 0.5), (-0.5, 0),(-0.5, -0.6)],
            [(0.5,-0.25),(1.1,0.4),(0.1,1),(-0.6,0.6),(-1,-0.5),(-0.5,-0.7)],
            [(0,-1),(1,-0.55),(0.5,0.5),(0.1,0.6),(0,1),(-0.4,1),(-0.5,0.3),(-1,0.1),(-0.7,-0.5),(-0.4,-0.5)]
        ),
        "LARGE": (
            [(0, -1), (0.8, -0.7), (0.9, 0), (1, 0.5), (0.5, 1), (-0.8, 0.5), (-0.5, 0), (-0.5, -0.6)],
            [(0.5, -0.25), (1.1, 0.4), (0.1, 1), (-0.6, 0.6), (-1, -0.5), (-0.5, -0.7)],
            [(0, -1), (1, -0.55), (0.5, 0.5), (0.1, 0.6), (0, 1), (-0.4, 1), (-0.5, 0.3), (-1, 0.1), (-0.7, -0.5),
             (-0.4, -0.5)],
            [(-0.9, 0.1), (-0.1, 1), (1, 0.1), (0.9, -1), (-0.1, -0.9)],
            [(-0.1, -0.9), (-0.9, 0.1), (-0.1, 1), (0, 0.9), (0.8, -0.7)]
        ),
        "MEDIUM": (
            [(0, 0.1), (1, 0.1), (1, 1), (-1, 0.6)],
            [(-1, 0.1), (0, 1), (1, 0.1), (0.5, -1), (-0.5, -0.7)],
            [(-0.9, 0.1), (-0.1, 1), (1, 0.1), (0.9, -1), (-0.1, -0.9)],
            [(0, 0.1), (1, 0.1), (-1, -1), (-1, 0.6)],
            [(-0.1, -0.9), (-0.9, 0.1), (-0.1, 1), (0, 0.9), (0.8, -0.7)]
        ),
        "SMALL": (
            [(0, 0.1), (1, 0.1), (1, 1), (-1, 0.6)],
            [(-1, 0.1), (0, 1), (1, 0.1), (0.5, -1), (-0.5, -0.7)],
            [(-0.9, 0.1), (-0.1, 1), (1, 0.1), (0.9, -1), (-0.1, -0.9)],
            [(0, 0.1), (1, 0.1), (-1, -1), (-1, 0.6)],
            [(-0.1, -0.9), (-0.9, 0.1), (-0.1, 1), (0, 0.9), (0.8, -0.7)]
        )

    }


class VectorRenderer(Renderer):

    def __init__(self,game):
        super().__init__(game)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 72)
        self.shipTimer = 0.2
        self.particles = []

    def renderAsteroid(self,astroid):
        #pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(astroid.position.x)),math.floor(getMP(astroid.position.y))),math.floor(getMP(Asteroid.ASTEROID_SIZES[astroid.size]["size"])));
        choices =len(ASTEROID_SHAPES[astroid.size])
        shape = []
        rot = math.radians(astroid.rotation)
        scale = Asteroid.ASTEROID_SIZES[astroid.size]["size"]

        for point in ASTEROID_SHAPES[astroid.size][astroid.appearance%choices]:
            shape.append(
        (getMP((math.cos(rot)*point[0]-math.sin(rot)*point[1])*scale+astroid.position.x),
         getMP(-(math.cos(rot)*point[1]+math.sin(rot)*point[0])*scale+astroid.position.y)))

        pygame.draw.polygon(self.screen,WHITE,shape)


    def renderVelocity(self,object):
        pygame.draw.aaline(self.screen,DEBUG_BLUE,
                           (getMP(object.position.x),getMP(object.position.y)),
                           (getMP(object.position.x+object.velocity.x),getMP(object.position.y+object.velocity.y)))

    def renderCollider(self,object):
        rad = object.getCollider()
        if rad is None:
            return

        pygame.draw.circle(self.screen,DEBUG_BLUE,(math.floor(getMP(object.position.x)),math.floor(getMP(object.position.y))),math.floor(getMP(rad)),min(2,math.floor(getMP(rad))));

    def renderShipAt(self,x,y,size,rotation):
        pygame.draw.polygon(self.screen,WHITE,
                            ((x+getMP(size*80)*math.cos(math.radians(rotation)),y+getMP(size*80)*math.sin(math.radians(rotation))),
                             (x+getMP(size*40)*math.cos(math.radians(rotation+120)),y+getMP(size*40)*math.sin(math.radians(rotation+120))),
                             (x,y),
                             (x+getMP(size*40)*math.cos(math.radians(rotation-120)),y+getMP(size*40)*math.sin(math.radians(rotation-120)))))

    def renderShip(self,ship,width,height):
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y)          ,ship.size,ship.rotation)
        self.renderShipAt(getMP(ship.position.x+width)  ,getMP(ship.position.y)          ,ship.size,ship.rotation)
        self.renderShipAt(getMP(ship.position.x-width)  ,getMP(ship.position.y)          ,ship.size,ship.rotation)
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y+height)   ,ship.size,ship.rotation)
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y-height)   ,ship.size,ship.rotation)

    def renderBullet(self,bullet):
        pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(bullet.position.x)),math.floor(getMP(bullet.position.y))),math.floor(getMP(5)));

    def renderParticle(self,particle):
        pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(particle.position.x)),math.floor(getMP(particle.position.y))),math.floor(getMP(5)));

    def render(self,game,delta):
        self.screen.fill(BLACK)
        if(game.ship.inV>0 and self.shipTimer<=0):
            self.shipTimer=0.2
        if(game.ship.inV>0):
            self.shipTimer-=delta
        else:
            self.shipTimer=0;


        for particle in self.particles:
            particle.updateMotion(delta)
            self.renderParticle(particle)
            if(not particle.alive):
                self.particles.remove(particle)

        if(game.ship.thrusting):
            self.particles.append(Particles.ParticleThruster(game.ship.position.x,game.ship.position.y,game.ship.rotation,game.ship.thrustScale))

        if(DEBUG):
            print("FPS:{:3.1f} {:3.1f}ms".format(1/delta,delta*1000))
            self.screen.blit(self.font.render("FPS:{:3.1f} {:3.1f}ms".format(1/delta,delta*1000),True,DEBUG_BLUE),(0,30))

        self.screen.blit(self.font.render("SCORE:{:3.0f}".format(game.score), True,WHITE),(0, 0))
        self.screen.blit(self.font.render("HP:{:3.0f}".format(game.hp), True,WHITE),(0, HEIGHT_P-72))
        for i in range(game.hp):
            self.renderShipAt(20+i*40, HEIGHT_P-72-20,0.5,-90)
        pygame.draw.circle(self.screen,WHITE,(0,0),10)
        for gameObject in game.gameObjects:
            if (isinstance(gameObject, Asteroid.Asteroid)):
                self.renderAsteroid(gameObject)
            if (isinstance(gameObject, Ship.Ship) and self.shipTimer<=0.1):
                self.renderShip(gameObject,game.WIDTH,game.HEIGHT)
            if (isinstance(gameObject, Bullet.Bullet)):
                self.renderBullet(gameObject)
            if (isinstance(gameObject, GameObj.ParticleEmiter)):
                if (DEBUG):
                    pygame.draw.circle(self.screen,DEBUG_PURPLE,(math.floor(getMP(gameObject.position.x)),math.floor(getMP(gameObject.position.y))),10)
                if(gameObject.emitCooldown<=0):
                    for i in range(gameObject.emitCount):
                        self.particles.append(gameObject.getParticle())
            if(DEBUG):
                    if(isinstance(gameObject,GameObj.GameObj)):
                        self.renderVelocity(gameObject)
                        self.renderCollider(gameObject)




        pygame.display.flip()

