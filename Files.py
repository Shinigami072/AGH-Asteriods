import math
import random
import pygame
import typing
from Model.ParticleEmitter import *

FONTS: typing.Dict[str, pygame.font.Font]={}
SOUNDS: typing.Dict[str, pygame.mixer.Sound]= {}
SOUNDSGROUP: typing.Dict[str, typing.Sequence[str]]= {}
NAMES :typing.Sequence[str] =[]
class ParticleEmitData:
    def __init__(self,type,data):
        self.type=type
        self.data=data
    def getParticleEmitter(self,parent):
        if self.type is None:
            return None

        if self.type == "ExE":
            return ExplosionEmitter(parent,(float)(self.data[0]))

        if self.type == "ThE":
            return Thruster(parent, (float)(self.data[0]),(float)(self.data[1]),(float)(self.data[2]),(float)(self.data[3]),(int)(self.data[4]),(float)(self.data[5]))

class Model:
    def __init__(self,name, model,particleEmitters={},particleGroups={}):
        self.name=name
        self.model=model
        self.particleEmitters=particleEmitters
        self.particleGroups=particleGroups
        Models[name]=self

    def getModel(self,x,y,rot=0,scale=1):
        rot = math.radians(-rot)

        d = [(x + (math.cos(rot) * a[0] - math.sin(rot) * a[1]) * scale,
              y - (math.cos(rot) * a[1] + math.sin(rot) * a[0]) * scale) for a in self.model]

        return d

    def __repr__(self):
        return "[M "+self.name+" ]:"+str(self.model)


class ModelGroup:
    def __init__(self , name :str, models):
        self.name = name
        self.models = models
        self.count = len(models)
        ModelGroups[name] = self
    def getModels(self):

        d =[Models[a] for a in self.models]
        return d
    def getRandomModel(self):
        return Models[random.choice(self.models)]
    def addModel(self,name):
        self.models.append(name)
        self.count += 1
    def removeModel(self,name):
        self.models.remove(name)
        self.count -= 1
    def __repr__(self):
        return "[G " + self.name + " ]{"+str(self.count)+"}:" + str(self.models)

Models: typing.Dict[str, Model]  = {}
def loadModel(file :str,name :str):
    model =[]
    particleEmitters = {}
    particleGroups ={}
    for line in file:
        if(line[0] == '#'):
            continue
        l = line.split(",")
        if l[0] == "VERTEX":
            model.append(
                ((float)(l[1]),(float)(l[2]))
            )
        if l[0] == "PARTICLE":
            particleEmitters[l[1].strip()]=ParticleEmitData(l[2].strip(),l[3].strip().split(":"))
        if l[0] == "PARTICLEGROUP":
            particleGroups[l[1].strip()]=l[2].strip().split(":")

    print(Model(name,model,particleEmitters,particleGroups))

ModelGroups: typing.Dict[str, ModelGroup]  = {}
def loadGroup(file,name):
    names =[]
    dir =file.name.replace(file.name.split("/")[-1],"",1)
    for line in file:
        if (line[0] == '#'):
            continue
        l = line.split(",")
        if l[0] == "MODEL":
           if(not l[2].strip() in Models.keys()):
               F = open(dir + l[1].strip())
               loadModel(F,l[2].strip())
           names.append(l[2].strip())

    print(ModelGroup(name,names))
def saveModel(file,model):
    for p in model.particleEmitters:
        partD = model.particleEmitters[p]
        datS = ":".join(model.particleEmitters[p].data)
        file.write("PARTICLE,{},{},{}\n".format(p, partD.type, datS))
    for pg in model.particleGroups:
        datS = ":".join(model.particleGroups[pg])
        file.write("PARTICLEGROUP,{},{}\n".format(pg, datS))

    for v in model.model:
        file.write("VERTEX,{},{}\n".format((v[0]),(v[1])))

def getSound(name):
    if name in SOUNDSGROUP:
        return SOUNDS[random.choice(SOUNDSGROUP[name])]
    elif name in SOUNDS:
        return SOUNDS[name]
    else:
        return None

def loadSound(file,name,volume):
    SOUNDS[name]=pygame.mixer.Sound(file)
    SOUNDS[name].set_volume(volume)

def loadData():

    modelList = open("files/models.index")
    for model in modelList:
        if (model[0] == '#'):
            continue
        l = model.split(",")
        if l[0] == "MODEL":
            F = open(l[1].strip())
            loadGroup(F, l[2].strip())

        if l[0] == "FONT":
            pygame.font.init()
            if (not l[1].strip() in FONTS.keys()):
                FONTS[l[1].strip()]=pygame.font.Font(l[2].strip(),(int)(l[3]))

        if l[0] == "FONT_DEFAULT":
            if (l[1].strip() in FONTS.keys()):
                FONTS["default"]=FONTS[l[1].strip()]

        if l[0] == "SOUND":
            if (l[1].strip() not in SOUNDS.keys()):
                loadSound(l[2].strip(),l[1].strip(),(float)(l[3].strip()))

        if l[0] == "SOUNDGROUP":
            if (l[1].strip() not in SOUNDSGROUP.keys()):
                SOUNDSGROUP[l[1].strip()]=l[2].strip().split(":")

    names = open("files/names")
    for name in names:
        NAMES.append(name.strip())


    print(FONTS.keys())
    print(SOUNDS.keys())