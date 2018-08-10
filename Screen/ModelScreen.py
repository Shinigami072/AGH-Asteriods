import pygame
import Screen.Screen
import View.ScreenRenderer as gui
from Files import Model
from Screen.GUI import *
import math
class ModelScreen(Screen.Screen.Screen):
    def __init__(self):
        super().__init__("model")
        self.useRenderer = False
        self.renderer = gui.ScreenRenderer(self.Width, self.Height)
        self.model=None
        self.Data = StringC("",0,0)
        self.guiObjects.append(self.Data)
        self.i=0
        self.scale=300
        self.x =0
        self.y =0
        self.rescale=0
        self.mode=0

    def changeTo(self,game):
        Files.loadModel(open("files/models/model"), "new")
        self.model = Files.Models["new"]
        self.i=0

    def save(self,name):
        F = open("files/models/"+name,mode="w")
        for p in self.model.particleEmitters:
            partD = self.model.particleEmitters[p]
            datS = ":".join(self.model.particleEmitters[p].data)
            F.write("PARTICLE,{},{},{}\n".format(p,partD.type,datS))
        for pg in self.model.particleGroups:
            datS=":".join(self.model.particleGroups[pg])
            F.write("PARTICLEGROUP,{},{}\n".format(pg,datS))

        for v in self.model.model:
            F.write("VERTEX,{},{}\n".format((v[0]+self.x)*(1+self.rescale/self.scale),(v[1]-self.y)*(1+self.rescale/self.scale)))
        F.close()

    def handleEvent(self,event):
        super().handleEvent(event)
        if(event.type == pygame.KEYDOWN):
            mul = 10 if event.mod&pygame.KMOD_SHIFT else 1
            mul =  0.1 if event.mod&pygame.KMOD_CTRL else mul
            if(event.key == pygame.K_RETURN):
                self.save("model")

            if (event.key == pygame.K_SLASH):
                Files.loadModel(open("files/models/model"),"new")
                self.model = Files.Models["new"]
                self.scale = 300
                self.x = 0
                self.y = 0
                self.rescale=0
            elif (event.key == pygame.K_2):
                self.model.model=[]
            elif (event.key == pygame.K_1):
                self.scale = 300
                self.x = 0
                self.y = 0
                self.rescale = 0
            elif (event.key == pygame.K_q):
                if( self.rescale+self.scale-0.05*mul!=0):
                    self.rescale -= 5 * mul
            elif (event.key == pygame.K_e):
                if( self.rescale+self.scale+0.05*mul!=0):
                    self.rescale += 5 * mul
            elif (event.key == pygame.K_w):
                self.y-=0.05*mul
            elif (event.key == pygame.K_s):
                self.y+=0.05 * mul
            elif (event.key == pygame.K_d):
                self.x +=0.05 * mul
            elif (event.key == pygame.K_a):
                self.x -=0.05 * mul
            elif(event.key == pygame.K_UP):
                if self.i-1*mul>0:
                    self.i-=1*mul
                else:
                    self.i=len(self.model.model)-1
            elif (event.key == pygame.K_DOWN):
                if self.i+1*mul < len(self.model.model)-1:
                    self.i += 1*mul
                else:
                    self.i=0
            elif (event.key == pygame.K_LEFT):
                if self.scale -1*mul> 0:
                    self.scale -= 1*mul
            elif (event.key == pygame.K_RIGHT):
                    self.scale += 1*mul
            print(event)
            pass
        if(event.type == pygame.MOUSEBUTTONUP):
            if(event.button ==1):
                posMa = event.pos
                posMo = (self.renderer.getMP(self.Width/2),self.renderer.getMP(self.Height/2))
                pos1 = ((posMa[0]-posMo[0])/self.scale,-(posMa[1]-posMo[1])/self.scale)
                print(posMa,posMo,pos1)
                self.model.model.insert(self.i,pos1)
            elif (event.button ==3 and len(self.model.model)>0):
                self.model.model.pop(self.i)
                if self.i > len(self.model.model) - 1:
                    self.i -= 1
                if self.i<0:
                    self.i=0

    def updateScreen(self,delta):
        shape = self.model.getModel(self.renderer.getMP(self.Width/2)+self.x*(self.scale+self.rescale),self.renderer.getMP(self.Height/2)+self.y*(self.scale+self.rescale),scale=(self.scale+self.rescale))
        self.Data.string="i={}/{} scale={} x={} y={}  resc={} mode={}".format(self.i+1,len(shape),self.scale,self.x,self.y,(1+self.rescale/self.scale),self.mode)

        if(len(shape)>2):
            pygame.draw.polygon(self.renderer.screen,(255,255,255),shape)
            pygame.draw.circle(self.renderer.screen,(200,200,255),(math.floor(shape[self.i][0]),math.floor(shape[self.i][1])),20,3)
        else:
            for p in shape:
                pygame.draw.circle(self.renderer.screen, (200, 200, 255),
                                   (math.floor(p[0]), math.floor(p[1])), 3, 3)

        pygame.draw.circle(self.renderer.screen, (200, 100, 255),
                           (math.floor(self.renderer.getMP(self.Width/2)),math.floor(self.renderer.getMP(self.Height/2))), 10, 1)
        pygame.draw.aaline(self.renderer.screen, (200, 100, 255),(0,self.renderer.getMP(self.Height/2)),(self.renderer.getMP(self.Width),self.renderer.getMP(self.Height/2)))
        pygame.draw.aaline(self.renderer.screen, (200, 100, 255),(self.renderer.getMP(self.Width/2),0),(self.renderer.getMP(self.Width/2),self.renderer.getMP(self.Height)))

        pygame.draw.circle(self.renderer.screen, (100, 200, 200),
                           (math.floor(self.renderer.getMP(self.Width/2)),math.floor(self.renderer.getMP(self.Height/2))),
                           math.floor(self.scale),
                           (0 if self.renderer.getMP(self.scale)<1 else 1)
                           )
