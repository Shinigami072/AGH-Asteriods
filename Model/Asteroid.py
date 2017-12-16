import pygame
import math
import random
from Model.GameObj import GameObj as GameObj

from pygame.math import Vector2

ASTEROID_SIZE = 60
ASTEROID_MASS = 100000
ASTEROID_SIZE_NAMES = ("XLARGE","LARGE","MEDIUM","SMALL")
ASTEROID_SIZES = {
    "XLARGE": {"size": ASTEROID_SIZE*1.5, "mass": 150 * ASTEROID_MASS, "points": 1, "maxCracks": 6,
              "minCracks": 5, "possibleCracks": ("LARGE", "LARGE", "LARGE", "MEDIUM", "MEDIUM", "SMALL")},
    "LARGE": {"size": ASTEROID_SIZE  , "mass": 25 * ASTEROID_MASS, "points": 1,"maxCracks":5,"minCracks":4,"possibleCracks":("MEDIUM","MEDIUM","MEDIUM","SMALL")},
    "MEDIUM": {"size": ASTEROID_SIZE/2, "mass": 5 * ASTEROID_MASS, "points": 5,"maxCracks":4,"minCracks":2,"possibleCracks":("SMALL","SMALL")},
    "SMALL": {"size": ASTEROID_SIZE/4, "mass": 1 * ASTEROID_MASS, "points": 10,"maxCracks":0,"minCracks":0, "possibleCracks":("SMALL","SMALL")}

}
class Asteroid(GameObj):
    def __init__(self,x,y, size=None):
        super().__init__(x,y);
        self.velocity = pygame.math.Vector2(random.random()*150,random.random()*150)
        if not size:
            self.size = random.choice(ASTEROID_SIZE_NAMES)
        else:
            self.size = size
        self.mass = ASTEROID_SIZES[self.size]["mass"]
        self.hit = False
        self.rotation = random.random()*360
        self.appearance = random.randint(0,128)
    def getCollider(self):
        return ASTEROID_SIZES[self.size]["size"]

    def crack(self,game,i):
        game.score +=  ASTEROID_SIZES[self.size]["points"]
        self.alive = False
        game.gameObjects.pop(i)


        print(game.score)
        newAsteroidMass = 0

        newAsteroidCount = random.randint(ASTEROID_SIZES[self.size]["minCracks"],ASTEROID_SIZES[self.size]["maxCracks"])
        possibleCracks = ASTEROID_SIZES[self.size]["possibleCracks"]
        if not newAsteroidCount>0:
            return
        astroAlpha = 360/newAsteroidCount
        while newAsteroidCount>0:
            newAsteroidCount-=1
            newAstrSize = random.choice(possibleCracks)
            print(newAstrSize)
            if(newAstrSize in possibleCracks):
                dist = random.random()
                newAstro = Asteroid(
                    self.position.x+math.cos(math.radians(astroAlpha*newAsteroidCount))*0.9*dist*ASTEROID_SIZES[self.size]["size"],
                    self.position.y+math.sin(math.radians(astroAlpha*newAsteroidCount))*0.9*dist*ASTEROID_SIZES[self.size]["size"],newAstrSize)
                newAstro.velocity = self.velocity.rotate(astroAlpha*newAsteroidCount)*(newAstro.mass/self.mass)
                newAstro.position += newAstro.velocity *0.1;
                #print(self.velocity,astroAlpha*newAsteroidCount,self.velocity.rotate(astroAlpha))
                game.gameObjects.append(newAstro)
"""      if (self.size / 2 > 0.05):
            aster1 = Asteroid(self.position.x, self.position.y)
            aster1.mass = self.mass / 2
            aster1.size = self.size / 2
            aster1.velocity = self.velocity.rotate(90) / 2

            aster2 = Asteroid(self.position.x, self.position.y)
            aster2.mass = self.mass / 2
            aster2.size = self.size / 2
            aster2.velocity = -aster1.velocity

            game.gameObjects[i] = aster1
            # game.gameObjects.append(aster1)
            game.gameObjects.append(aster2)"""


   # def isInside(self,x,y,radius):
   #     pos2 = pygame.math.Vector2(x,y)
   #     dist = pos2-self.position
   #
   #    return (dist.length()<radius+self.size*ASTEROID_SIZE)