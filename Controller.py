import pygame
import math
from pygame.math import Vector2

inputRotation = 0
inputVector = Vector2(0, 0)
rotJoyVector = Vector2(0, 0)
rotKey =0
menuSelector=0
menuActivate =False

keyboard=True
controller=False
keyboardRedirect=False

conMenuVal=0;
inputButtons = {"shot": False,"pause":False,"debug": False,"inV": False,"scr": False,"shw": False}

keyBindings ={
    "Controller":{
        "menu_UP":-1,
        "menu_DOWN":-1,
        "menu_Confirm":0,

        "game_pause": 7,
        "debug":6

        #"shot":0
    },
    "Keyboard":{
                "menu_UP":pygame.K_w,
                "menu_DOWN":pygame.K_s,
                "menu_Confirm":pygame.K_d,

                "game_pause":pygame.K_ESCAPE,
                "move_UP":pygame.K_w,
                "move_DOWN":pygame.K_s,
                "move_LEFT":pygame.K_a,
                "move_RIGHT":pygame.K_d,
                "rot_LEFT": pygame.K_q,
                "rot_RIGHT":pygame.K_e,
                "shot":pygame.K_SPACE,

                "debug": pygame.K_c

    },

}

#Translacja wszyskich eventów wejściowych, na dane kontrolujace

#ustawienie danych ruchu
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
def handleRotation(rotation):
    global inputRotation
    inputRotation = rotation

    while(inputRotation<0 or inputRotation>=360):
        if(inputRotation<0):
            inputRotation=inputRotation+360
        if (inputRotation >= 360):
            inputRotation = inputRotation-360

def eventHandle(event):
    global rotKey
    global menuSelector
    global menuActivate
    global keyboard
    global controller
    global conMenuVal
    #wszykie eveny wciśnięcia przycisku
    if(event.type == pygame.KEYDOWN and not keyboardRedirect):
        controller=False
        keyboard=True
        if (event.key == keyBindings["Keyboard"]["menu_UP"]):
            menuSelector-=1
        if (event.key == keyBindings["Keyboard"]["menu_DOWN"]):
            menuSelector += 1
        if (event.key == keyBindings["Keyboard"]["menu_Confirm"]):
            menuActivate=True
        if(event.key == keyBindings["Keyboard"]["move_UP"]):
            handleMovement(inputVector.x,inputVector.y+1);
        if(event.key == keyBindings["Keyboard"]["move_DOWN"]):
            handleMovement(inputVector.x,inputVector.y-1);
        if(event.key == keyBindings["Keyboard"]["move_LEFT"]):
            handleMovement(inputVector.x-1,inputVector.y);
        if(event.key == keyBindings["Keyboard"]["move_RIGHT"]):
            handleMovement(inputVector.x+1,inputVector.y);
        if (event.key == keyBindings["Keyboard"]["rot_LEFT"]):
            rotKey=-1
        if (event.key == keyBindings["Keyboard"]["rot_RIGHT"]):
            rotKey =1
        if(event.key == keyBindings["Keyboard"]["shot"]):
            inputButtons["shot"]=True

        if (event.key == pygame.K_x):
            inputButtons["scr"] = True
        if (event.key == pygame.K_z):
            inputButtons["shw"] = True
        if (event.key == keyBindings["Keyboard"]["game_pause"]):
            inputButtons["pause"] = not inputButtons["pause"]
        if (event.key == keyBindings["Keyboard"]["debug"]):
            inputButtons["debug"] = not inputButtons["debug"]
        if (event.key == pygame.K_i):
            inputButtons["inV"] = True

    #wszyskie evety podniesienia przycisku
    if(event.type == pygame.KEYUP):
        if (event.key == keyBindings["Keyboard"]["menu_Confirm"]):
            menuActivate = False
        if(event.key == keyBindings["Keyboard"]["move_UP"]):
            handleMovement(inputVector.x,inputVector.y-1);
        if(event.key == keyBindings["Keyboard"]["move_DOWN"]):
            handleMovement(inputVector.x,inputVector.y+1);
        if(event.key == keyBindings["Keyboard"]["move_LEFT"]):
            handleMovement(inputVector.x+1,inputVector.y);
        if(event.key == keyBindings["Keyboard"]["move_RIGHT"]):
            handleMovement(inputVector.x-1,inputVector.y);
        if (event.key == keyBindings["Keyboard"]["rot_LEFT"] or event.key == keyBindings["Keyboard"]["rot_RIGHT"]):
            rotKey = 0
        if (event.key == pygame.K_x):
            inputButtons["scr"] = False
        if (event.key == pygame.K_z):
            inputButtons["shw"] = False
        if(event.key == keyBindings["Keyboard"]["shot"]):
            inputButtons["shot"]=False
        if (event.key == pygame.K_i):
            inputButtons["inV"] = False

    #ebenty kontrollera
    if(event.type == pygame.JOYAXISMOTION):
        controller=True
        keyboard=False
        value = event.value

        #ustawienie deadspace - ignorowanych wartości
        if math.fabs(value) < 0.07:
            value=0

        #lewy joystick
        if(event.axis ==0):
            if math.fabs(value) < 0.3:
                 value=0


            handleMovement(value,inputVector.y)
        elif(event.axis ==1):
            if math.fabs(value) < 0.07:
                value=0

            if(math.fabs(conMenuVal)<=0.3):
                if value > 0.5:
                    conMenuVal=1
                    menuSelector += 1
                elif value < -0.5:
                    menuSelector -= 1
                    conMenuVal=-1
            else:
                conMenuVal=value
            handleMovement(inputVector.x,-value)

        #prawy joysick
        elif(event.axis == 3 or event.axis==4):
            global rotJoyVector
            if(event.axis == 3):
                rotJoyVector.x = value
            elif(event.axis==4):
                rotJoyVector.y = -value

            if(rotJoyVector.length() >0.5):
                handleRotation(rotJoyVector.angle_to(pygame.math.Vector2(1,0)))

        #prawy trigger
        elif (event.axis == 5):
            if math.fabs(value) < 0.07:
                value=0
            if(value >0.6):
                inputButtons["shot"] = True
            else:
                inputButtons["shot"] = False
        else:
            pass
            #print(event,event.axis,event.value)
    #przyciski kontrollera
    if(event.type == pygame.JOYBUTTONDOWN):
        controller=True
        keyboard=False
        if (event.button ==  keyBindings["Controller"]["menu_Confirm"]):
            menuActivate=True
        if (event.button == keyBindings["Controller"]["game_pause"]):
            inputButtons["pause"] = not inputButtons["pause"]

        if(event.button == keyBindings["Controller"]["debug"]):
            inputButtons["debug"] = not inputButtons["debug"]
        else:
            print(event,event.button)

    if(event.type == pygame.JOYBUTTONUP):
        if (event.button == keyBindings["Controller"]["menu_Confirm"]):
            menuActivate = False

    #d-pad kontrollera
    if(event.type == pygame.JOYHATMOTION):
        controller=True
        keyboard=False
        if(event.hat == 0 ):
            menuSelector -= event.value[1]
        else:
            print(event,event.hat, event.value)