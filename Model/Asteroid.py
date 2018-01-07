import pygame
import math
import random
from Model.GameObj import GameObj
from Model.LootBox import LootBox
import Files
import Sound
from pygame.math import Vector2
#obiekt asteroida
ASTEROID_SIZE = 60
ASTEROID_MASS = 100000
ASTEROID_SIZE_NAMES = ("XLARGE","LARGE","MEDIUM","SMALL")
ASTEROID_SIZES = {
    "XLARGE": {"size": ASTEROID_SIZE*1.5, "mass": 18 * ASTEROID_MASS, "points": 1,"velocity":15, "maxCracks": 6,
              "minCracks": 5, "possibleCracks": ("LARGE", "LARGE", "LARGE", "MEDIUM", "MEDIUM", "SMALL")},
    "LARGE": {"size": ASTEROID_SIZE  , "mass":  16 * ASTEROID_MASS, "points": 1,"velocity":30,"maxCracks":5,"minCracks":4,"possibleCracks":("MEDIUM","MEDIUM","MEDIUM","SMALL")},
    "MEDIUM": {"size": ASTEROID_SIZE/2, "mass": 4 * ASTEROID_MASS, "points": 5,"velocity":60,"maxCracks":4,"minCracks":2,"possibleCracks":("SMALL","SMALL")},
    "SMALL": {"size": ASTEROID_SIZE/4, "mass": 2 * ASTEROID_MASS, "points": 10,"velocity":90,"maxCracks":0,"minCracks":0, "possibleCracks":None}

}
#przechowywanie danych o asteroidach
class Asteroid(GameObj):
    count =0;
    def __init__(self,x,y, size=None):
        super().__init__(x,y);
        if not size:
            self.size = random.choice(ASTEROID_SIZE_NAMES)
        else:
            self.size = size
        self.velocity = pygame.math.Vector2(ASTEROID_SIZES[self.size]["size"],0).rotate(random.random()*360)
        self.mass = ASTEROID_SIZES[self.size]["mass"]
        self.hit = False
        self.rotation = random.random()*360
        self.rotVel = random.choice([-1,1])*random.random()*15
        self.appearance = random.randint(0,128)
        self.setModel(Files.ModelGroups.get("asteroid"+size).getRandomModel())
        self.particleEmitters["explode"].active=False

    def getCollider(self):
        return ASTEROID_SIZES[self.size]["size"]
    def add(self):
        Asteroid.count+=1
        return self
    #co zrobić w wypadku gdy rozpada się asteroida
    def crack(self,game,i):
        #dodanie odpowiedniej ilości punktów
        game.score +=  ASTEROID_SIZES[self.size]["points"]

        #przygotowanie do usunięcia oryginalnej asteroidy i aktywoawnie emitera cząsteczek
        self.alive = False
        Asteroid.count-=1
        self.particleEmitters["explode"].active=True
        Sound.playSound("explode_0")
        #wyjście z funkcji jeżeli nie mamy na co się rozpaść
        if ASTEROID_SIZES[self.size]["possibleCracks"] is None :
            return
        if(random.random()<0.1):
            game.gameObjects.append(LootBox(self.position.x,self.position.y,game))
        newAsteroidMass = 0
        asteroids = []
        #dodawanie asteroid aż mamy masę
        while(newAsteroidMass <self.mass):
            #losowy rozmiar asteroidy
            a = Asteroid(self.position.x,self.position.y,random.choice(ASTEROID_SIZES[self.size]["possibleCracks"]))
            #sprawdzenie czy sięzmieści
            if(newAsteroidMass+a.mass <=self.mass):
                #przesunięcie w losowe miejsce
                a.position.x+=random.choice([-1.1])*0.6*random.random()*ASTEROID_SIZES[self.size]["size"]
                a.position.y+=random.choice([-1.1])*0.6*random.random()*ASTEROID_SIZES[self.size]["size"]
                newAsteroidMass +=a.mass

                #umiejscowienie asteroidy w miejscu nie zajętym przez inna dodawaną asteroidę
                isDone =False
                while(not isDone):
                    isDone=True
                    for b in asteroids:
                        if(a.checkCollision(b)):
                            isDone=False
                            a.position.x=b.position.x+random.choice([ASTEROID_SIZES[b.size]["size"]+ASTEROID_SIZES[a.size]["size"],-ASTEROID_SIZES[a.size]["size"]-ASTEROID_SIZES[b.size]["size"]])
                            a.position.y=b.position.y+random.choice([ASTEROID_SIZES[b.size]["size"]+ASTEROID_SIZES[a.size]["size"],-ASTEROID_SIZES[a.size]["size"]-ASTEROID_SIZES[b.size]["size"]])


                a.velocity = ASTEROID_SIZES[a.size]["velocity"]*(a.position-self.position)/ASTEROID_SIZES[self.size]["size"]
                a.velocity+= self.velocity
                asteroids.append(a)

        #dodanie nowych asteroid
        for a in asteroids:
            game.gameObjects.append(a.add())