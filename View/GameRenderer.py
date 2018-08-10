from View.Renderer import *
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

class VectorRenderer(Renderer):

    def __init__(self,width,height):
        super().__init__(width,height)
        self.M_TO_P = max((width-80)/WIDTH_P,(height-80)/HEIGHT_P)
        self.shipTimer = 0.2
        self.lootTimer = 0.2
        self.scoreTimer=1
        self.score=0
        self.particles = []
        self.particleCount=0;

    def updateRendererData(self, game, delta):

        if (game.ship.inV > 0 and self.shipTimer <= 0):
            self.shipTimer = 0.3
        if (game.ship.inV > 0):
            self.shipTimer -= delta
        else:
            self.shipTimer = 0;

        if (self.lootTimer > 0):
            self.lootTimer -= delta
        else:
            self.lootTimer = 7.5;

    def renderModel(self,model,Color,x,y,scale=1,rot=0):
        shape = model.getModel(x,y,rot=rot,scale=scale)
        pygame.gfxdraw.aapolygon(self.screen, shape, Color)
        pygame.gfxdraw.filled_polygon(self.screen, shape, Color)

    def renderGameObj(self,gameObj,WIDTH,HEIGHT):
        scale = self.getMP(gameObj.scale)
        bias =self.getMP(gameObj.bias)
        x = self.getMP(gameObj.position.x)
        y = self.getMP(gameObj.position.y)
        self.renderModel(
            gameObj.model,
            WHITE,
            x,
            y,
            scale,
            gameObj.rotation)

        if(HEIGHT_P-y<scale-bias):
            self.renderModel(
                gameObj.model,
                WHITE,
                x,
                self.getMP(-2*gameObj.bias-(HEIGHT-(gameObj.position.y))),
                scale,
                gameObj.rotation)
        elif(y<scale-bias):
            self.renderModel(
                gameObj.model,
                WHITE,
                x,
                self.getMP(HEIGHT+2*gameObj.bias + (gameObj.position.y)),
                scale,
                gameObj.rotation)

        if (WIDTH_P - x < scale-bias):
            self.renderModel(
                gameObj.model,
                WHITE,
                self.getMP(-2*gameObj.bias-(WIDTH-gameObj.position.x)),
                y,
                scale,
                gameObj.rotation)
        elif (x < scale-bias):
            self.renderModel(
                gameObj.model,
                WHITE,
                self.getMP(WIDTH+2*gameObj.bias + gameObj.position.x),
                y,
                scale,
                gameObj.rotation)

    def renderCircle(self,Color,pos,rad,width=None):
        if(width is None):
            width=min(2, math.floor(self.getMP(rad)))
        pygame.draw.circle(self.screen,Color,(math.floor(self.getMP(pos[0])),math.floor(self.getMP(pos[1]))),math.floor(self.getMP(rad)),width);

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


    def renderCollider(self,object):
        rad = object.getCollider()
        if rad is None:
            return
        self.renderCircle(DEBUG_BLUE,object.position,rad)

    def renderShipAt(self,x,y,size,rotation):
        m = Files.Models["Classic"]
        self.renderModel(m,GRAY,x+3,y+3,size,rotation)
        self.renderModel(m,WHITE,x,y,size,rotation)



    def renderShip(self,ship,WIDTH,HEIGHT):
        if(self.shipTimer<0.2 and not ship.dead):
            self.renderGameObj(ship,WIDTH,HEIGHT)


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


    def renderBullet(self,bullet):
        self.renderCircle(WHITE,bullet.position,bullet.getCollider())

    def renderEnemy(self, enemy,WIDTH,HEIGHT):
        self.renderGameObj(enemy,WIDTH,HEIGHT)
        if (enemy.AI.mode == "DESTROY"):
            pygame.draw.aaline(self.screen, GRAY,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + self.getMP(enemy.AI.searchdist) * math.cos(
                                   math.radians(enemy.rotation - enemy.AI.timer2*enemy.AI.shotangle)),
                                self.getMP(enemy.position.y) + self.getMP(enemy.AI.searchdist) * math.sin(
                                    math.radians(enemy.rotation - enemy.AI.timer2*enemy.AI.shotangle)))
                               )
            pygame.draw.aaline(self.screen, GRAY,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + self.getMP(enemy.AI.searchdist) * math.cos(
                                   math.radians(enemy.rotation + enemy.AI.timer2 * enemy.AI.shotangle)),
                                self.getMP(enemy.position.y) + self.getMP(enemy.AI.searchdist) * math.sin(
                                    math.radians(enemy.rotation + enemy.AI.timer2 * enemy.AI.shotangle)))
                               )
        if (self.DEBUG):
            c = WHITE
            if(enemy.AI.mode == "IDLE"):
                c= DEBUG_PURPLE
            elif (enemy.AI.mode == "SEARCH"):
                c = DEBUG_BLUE
            elif (enemy.AI.mode == "DESTROY"):
                c = DEBUG_YELLOW

            self.renderCircle(c,enemy.position,90,12)


            pygame.draw.aaline(self.screen,DEBUG_BLUE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x )+self.getMP(enemy.AI.searchdist)* math.cos(math.radians(enemy.rotation+enemy.AI.searchangle)),
                                self.getMP(enemy.position.y)+ self.getMP(enemy.AI.searchdist)*math.sin(math.radians(enemy.rotation+enemy.AI.searchangle)))
                               )
            pygame.draw.aaline(self.screen, DEBUG_BLUE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + self.getMP(enemy.AI.searchdist) * math.cos(math.radians(enemy.rotation - enemy.AI.searchangle)),
                                self.getMP(enemy.position.y) + self.getMP(enemy.AI.searchdist) * math.sin(math.radians(enemy.rotation - enemy.AI.searchangle)))
                               )
            pygame.draw.aaline(self.screen, DEBUG_PURPLE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + self.getMP(enemy.AI.searchdist) * math.cos(
                                   math.radians(enemy.rotation + enemy.AI.shotangle)),
                                self.getMP(enemy.position.y) + self.getMP(enemy.AI.searchdist) * math.sin(
                                    math.radians(enemy.rotation + enemy.AI.shotangle)))
                               )
            pygame.draw.aaline(self.screen, DEBUG_PURPLE,
                               (self.getMP(enemy.position.x), self.getMP(enemy.position.y)),
                               (self.getMP(enemy.position.x) + self.getMP(enemy.AI.searchdist) * math.cos(
                                   math.radians(enemy.rotation - enemy.AI.shotangle)),
                                self.getMP(enemy.position.y) + self.getMP(enemy.AI.searchdist) * math.sin(
                                    math.radians(enemy.rotation - enemy.AI.shotangle)))
                               )
            self.renderCircle(c,enemy.AI.target,12,0)


    def renderLootBox(self,lootbox):
        rot = lootbox.rotation
        scale = self.getMP(lootbox.scale)

        self.renderModel(lootbox.model, WHITE, self.getMP(lootbox.position.x), self.getMP(lootbox.position.y), scale, rot)
        self.renderModel(lootbox.typeModel, GRAY, self.getMP(lootbox.position.x), self.getMP(lootbox.position.y), scale, rot)

        if(self.lootTimer<1) and self.lootTimer>=0:
            lootscale = (1-(self.lootTimer)/1)
            rad=200*lootscale
            #draw radar Pulse
            pygame.draw.circle(self.screen,(BLACK.lerp(WHITE,1-lootscale)),(math.floor(self.getMP(lootbox.position.x)),math.floor(self.getMP(lootbox.position.y))),math.floor(rad),6 if rad>6 else 0);



    def renderParticle(self,particle):
        if(isinstance(particle,Particles.FireParticle)):
            self.renderCircle((BLACK.lerp(WHITE,0.8+0.2*particle.getlifeP())), particle.position, 5*particle.scale,width=0)
        else:
            self.renderCircle((BLACK.lerp(WHITE,particle.getlifeP())), particle.position, 5*particle.scale,width=0)

    def handleParticleEmitter(self,particleEmitter,delta):
        particleEmitter.update(delta)
        if (self.DEBUG):
            self.renderCircle(DEBUG_PURPLE,particleEmitter.getPosition(),5,0)
        if(particleEmitter.emitCooldown<=0 and self.particleCount<1000 and particleEmitter.active):
            for i in range(particleEmitter.emitCount):
                if(self.particleCount<1000):
                    p = particleEmitter.getParticle()
                    if not p is None:
                        self.particles.append(p)
    def renderString(self,string,x,y,Colorfg=WHITE,Colorbg=GRAY):
        offset =0;
        height = self.font.size(string)[1]
        for line in string.splitlines():
            if line[0] != "#":
                self.screen.blit(self.font.render(line, True,  Colorbg), (x+3, y+offset+3))
                self.screen.blit(self.font.render(line, True, Colorfg), (x, y+offset))
                offset += height

            else:
                self.screen.blit(Files.FONTS["mono-24"].render(line, True, DEBUG_BLUE), (x, y+offset))
                offset+=24


    def renderHUD(self,game,delta):

        if (self.score < game.score):
            self.scoreTimer -= delta
            if (self.score + (1 - self.scoreTimer) * (game.score - self.score) >= game.score):
                self.score = game.score
                self.scoreTimer = 1

            score = math.floor(self.score + (1 - self.scoreTimer) * (game.score - self.score))
        else:
            score = game.score

        hudString = "SCORE:{:07.0f}\n".format(score)
        hudString += "Level:{:-3d}\n".format(game.level())

        if (self.DEBUG):
            hudString +="#FPS:{:03.1f} {:-3.0f}ms\n".format(1 / delta, delta * 1000)
            hudString +="#Objects         :{:-3d}\n".format(len(game.gameObjects))
            hudString +="#truescore       :{:-7d}\n".format(game.score)
            hudString +="#spawnedAsteroids:{:-3d}\n".format(game.spawnedAsteroids)
            hudString +="#spawnedEnemies  :{:-3d}\n".format(game.spawnedEnemies)
            hudString +="#addedlife       :{:-3d}\n".format(game.addedLife)
            hudString +="#destroyAsteroids:{:-3d}\n".format(game.destroyedAsteroids)
            hudString +="#Asteroid.count  :{:-3d}\n".format(Asteroid.Asteroid.count)
            hudString +="#Inv             :{:-2.2f}\n".format(game.ship.inV)

        self.renderString(hudString,0,0)
        self.renderString("HP:{:3.0f}".format(game.hp),0,HEIGHT_P - 72)
        self.font =Files.FONTS["cow-48"]
        self.renderString("\n".join(game.messages),WIDTH_P-400,0)
        self.font =Files.FONTS["default"]
        if(len(game.messages)>0):
            game.msgTimer-=delta
        if(game.msgTimer<0):
            game.messages.pop(0)
            game.msgTimer=1
        if game.ship.dead:
            str = "Press {} to use Repair Kit [{}]".format(Controller.getName("revive"),game.hp)
            width = self.font.size(str)[0]
            self.renderString(str, (WIDTH_P-width)/ 2, HEIGHT_P/2)
        for i in range(game.hp):
            self.renderShipAt(20 + i * 40, HEIGHT_P - 72 - 20, 20, -90)

    def renderMain(self,game,delta):
        #Symulacja Cząsteczek
        self.particleCount = len(self.particles)
        for particle in self.particles:
            if (not Controller.inputButtons["pause"]):
                particle.updateMotion(delta)
            self.renderParticle(particle)
            if (not particle.alive):
                self.particles.remove(particle)

        for gameObject in game.gameObjects:
            if (isinstance(gameObject, Ship.Ship) and self.shipTimer <= 0.5):
                self.renderShip(gameObject,game.WIDTH,game.HEIGHT)
            elif (isinstance(gameObject, Bullet.Bullet)):
                self.renderBullet(gameObject)
            elif (isinstance(gameObject, Enemy)):
                self.renderEnemy(gameObject,game.WIDTH,game.HEIGHT)
            elif (isinstance(gameObject, LootBox)):
                self.renderLootBox(gameObject)
            else:
                self.renderGameObj(gameObject,game.WIDTH,game.HEIGHT)

            if (self.DEBUG):
                if (isinstance(gameObject, GameObj.GameObj)):
                    self.renderVelocity(gameObject)
                    self.renderCollider(gameObject)
                    if (not isinstance(gameObject, Ship.Ship)):
                        self.renderRotation(gameObject)

            #Handle Particles
            if (not Controller.inputButtons["pause"]):
                for particleEmitter in gameObject.particleEmitters:
                    self.handleParticleEmitter(gameObject.particleEmitters[particleEmitter], delta)

    def render(self,game,delta):
        self.font = Files.FONTS["default"]



        self.updateRendererData(game,delta)
        self.renderMain(game,delta)
        self.renderHUD(game,delta)