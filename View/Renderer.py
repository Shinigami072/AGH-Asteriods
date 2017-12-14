import pygame
import math
import Model.Asteroid as Asteroid
import Model.Bullet as Bullet
import Model.GameObj as GameObj
import Model.Ship as Ship

FPS = 60
#HEIGHT_P = 720
#WIDTH_P = 1280
HEIGHT_P = 1080
WIDTH_P = 1920
M_TO_P = 10

BLACK = (0,0,0)
WHITE = (255,255,255)
DEBUG_BLUE = (0,220,220)
DEBUG = True

def getMP(m):
    return m/M_TO_P

class Renderer:

    def __init__(self,game):
        global M_TO_P
        global WIDTH_P
        global HEIGHT_P

        M_TO_P = max(game.WIDTH/WIDTH_P,game.HEIGHT/HEIGHT_P)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_P, HEIGHT_P))
        self.clock = pygame.time.Clock()

    def render(self,game):
        pass

class VectorRenderer(Renderer):


    def renderAsteroid(self,astroid):
        pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(astroid.position.x)),math.floor(getMP(astroid.position.y))),math.floor(getMP(astroid.size*60)));

    def renderVelocity(self,object):
        pygame.draw.aaline(self.screen,DEBUG_BLUE,
                           (getMP(object.position.x),getMP(object.position.y)),
                           (getMP(object.position.x+object.velocity.x),getMP(object.position.y+object.velocity.y)))

    def renderCollider(self,object):
        pygame.draw.circle(self.screen,DEBUG_BLUE,(math.floor(getMP(object.position.x)),math.floor(getMP(object.position.y))),math.floor(getMP(object.getCollider())),min(2,math.floor(getMP(object.getCollider()))));

    def renderShipAt(self,x,y,ship):
        pygame.draw.polygon(self.screen,WHITE,
                            ((x+getMP(ship.size*80)*math.cos(math.radians(ship.rotation)),y+getMP(ship.size*80)*math.sin(math.radians(ship.rotation))),
                             (x+getMP(ship.size*40)*math.cos(math.radians(ship.rotation+120)),y+getMP(ship.size*40)*math.sin(math.radians(ship.rotation+120))),
                             (x,y),
                             (x+getMP(ship.size*40)*math.cos(math.radians(ship.rotation-120)),y+getMP(ship.size*40)*math.sin(math.radians(ship.rotation-120)))))

    def renderShip(self,ship,width,height):
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y)          ,ship)
        self.renderShipAt(getMP(ship.position.x+width)  ,getMP(ship.position.y)          ,ship)
        self.renderShipAt(getMP(ship.position.x-width)  ,getMP(ship.position.y)          ,ship)
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y+height)   ,ship)
        self.renderShipAt(getMP(ship.position.x)        ,getMP(ship.position.y-height)   ,ship)
       # pygame.draw.aaline(screen,(0,220,220),(self.position.x,self.position.y),(self.position.x+self.velocity.x,self.position.y+self.velocity.y))
        #pygame.draw.circle(screen,(0,220,220),(math.floor(self.position.x),math.floor(self.position.y)),math.floor(self.getCollider()),1)
    def renderBullet(self,bullet):
        pygame.draw.circle(self.screen,WHITE,(math.floor(getMP(bullet.position.x)),math.floor(getMP(bullet.position.y))),math.floor(getMP(5)));
    def render(self,game):
        self.screen.fill(BLACK)
        pygame.draw.circle(self.screen,WHITE,(0,0),10)
        for gameObject in game.gameObjects:
            if (isinstance(gameObject, Asteroid.Asteroid)):
                self.renderAsteroid(gameObject)
            if (isinstance(gameObject, Ship.Ship)):
                self.renderShip(gameObject,game.WIDTH,game.HEIGHT)
            if (isinstance(gameObject, Bullet.Bullet)):
                self.renderBullet(gameObject)
            if(DEBUG):
                    if(isinstance(gameObject,GameObj.GameObj)):
                        self.renderVelocity(gameObject)
                        self.renderCollider(gameObject)




        pygame.display.flip()

