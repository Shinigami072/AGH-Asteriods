import pygame
import math
from pygame.math import Vector2


inputVector = Vector2(0, 0)
inputButtons = {"shot": False,"debug": False,"inV": False}



def handleMovement(x,y):
    global inputVector
    inputVector.x=x
    inputVector.y=y
    if(inputVector.x>1):
        inputVector.x=1
    if(inputVector.x<-1):
        inputVector.x=-1

    if(inputVector.y>1):
        inputVector.y=1
    if(inputVector.y<-1):
        inputVector.y=-1


def eventHandle(event):
    if(event.type == pygame.KEYDOWN):
        if(event.key == pygame.K_UP):
            handleMovement(inputVector.x,inputVector.y+1);
        if(event.key == pygame.K_DOWN):
            handleMovement(inputVector.x,inputVector.y-1);
        if(event.key == pygame.K_LEFT):
            handleMovement(inputVector.x-1,inputVector.y);
        if(event.key == pygame.K_RIGHT):
            handleMovement(inputVector.x+1,inputVector.y);
        if(event.key == pygame.K_SPACE ):
            inputButtons["shot"]=True
        if (event.key == pygame.K_d):
            inputButtons["debug"] = True
        if (event.key == pygame.K_i):
            inputButtons["inV"] = True
    if(event.type == pygame.KEYUP):
        if(event.key == pygame.K_UP):
            handleMovement(inputVector.x,inputVector.y-1);
        if(event.key == pygame.K_DOWN):
            handleMovement(inputVector.x,inputVector.y+1);
        if(event.key == pygame.K_LEFT):
            handleMovement(inputVector.x+1,inputVector.y);
        if(event.key == pygame.K_RIGHT):
            handleMovement(inputVector.x-1,inputVector.y);
        if(event.key == pygame.K_SPACE ):
            inputButtons["shot"]=False
        if (event.key == pygame.K_d):
            inputButtons["debug"] = False
        if (event.key == pygame.K_i):
            inputButtons["inV"] = False

    if(event.type == pygame.JOYAXISMOTION):
        print(event.value,inputVector)
        value = event.value
        if math.fabs(value) < 0.07:
            value=0
        if(event.axis ==0):
            if math.fabs(value) < 0.3:
                 value=0
            handleMovement(value*0.8,inputVector.y)
        elif(event.axis ==1):
            if math.fabs(value) < 0.07:
                value=0
            handleMovement(inputVector.x,-value)

        elif(event.axis == 3 or event.axis==4):
            pass

        elif (event.axis == 5):
            if math.fabs(value) < 0.07:
                value=0
            if(value >0.6):
                inputButtons["shot"] = True
            else:
                inputButtons["shot"] = False

        else:
            print(event,event.axis,event.value)

    if(event.type == pygame.JOYBUTTONDOWN):
        print(event,event.button)


    if(event.type == pygame.JOYHATMOTION):
        print(event,event.hat, event.value)