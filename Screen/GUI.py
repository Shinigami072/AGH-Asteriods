from View.Renderer import *
import Files
import Sound
import Controller


class StringC:
    def __init__(self,string,x,y,color=WHITE,font="default",scale=12):
        self.color = color
        self.font=font
        self.string=string
        self.x=x
        self.y=y
        self.height = Files.FONTS[font].size(string)[1]/scale
        self.visible=True

class Input:
    def __init__(self, string, x, y, width, height, font="default",color=WHITE, id=0,
                 menuCount=1, scale=12,maxwidth=-1):
        self.string = StringC(string, x, y, WHITE, scale=scale,font=font)
        self.string.x = x + 0.5
        self.string.y = y + height - self.string.height

        self.visible = True
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = 0
        self.id = id
        self.menuCount = menuCount
        self.maxwidth=maxwidth

    def isInside(self,mousepos):
        return (self.x <= mousepos[0] and self.x+self.width>=mousepos[0]) and (self.y <= mousepos[1] and self.y+self.height>=mousepos[1])

    def update(self, mousepos, mousebut):
        if (not self.visible):
            return

        if (self.state == 0):
            self.string.color = WHITE
        elif self.state ==2:
            self.string.color = (144,144,144)
        else:
            self.string.color = BLACK

        if (Controller.keyboard or Controller.controller):
            self.updateC()
            return
        if(self.state !=2):
            if (self.isInside(mousepos)):

                if (self.state != 1):
                    Sound.playSound("change")
                self.state = 1
            else:
                self.state = 0
        elif mousebut[0] and not self.isInside(mousepos):
            self.state = 0
            Controller.keyboardRedirect=False


        if (self.state != 0 and (mousebut[0])):
            self.activate()

    def updateText(self,u):
        print(u,self.state)
        if not (self.visible and self.state == 2):
            return
        print(u)
        if u == "\r":
            self.state = 0
            Controller.keyboardRedirect=False
        elif u == "\x08":
            self.string.string=self.string.string[:-1]
        elif u.isprintable() and (self.maxwidth<0 or len(self.string.string)<self.maxwidth):
            self.string.string+=u

    def activate(self):
        self.state = 2
        Controller.keyboardRedirect = True

    def updateC(self):
        if(self.state ==2):
            return

        if Controller.menuSelector % self.menuCount == self.id:
            if self.state != 1:
                Sound.playSound("change")
            self.state = 1
        else:
            self.state = 0

        if self.state == 1 and Controller.menuActivate:
            Controller.menuActivate = False
            self.activate()


class Input:
    def __init__(self, string, x, y, width, height, font="default",color=WHITE, id=0,
                 menuCount=1, scale=12,maxwidth=-1):
        self.string = StringC(string, x, y, WHITE, scale=scale,font=font)
        self.string.x = x + 0.5
        self.string.y = y + height - self.string.height

        self.visible = True
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = 0
        self.id = id
        self.menuCount = menuCount
        self.maxwidth=maxwidth

    def isInside(self,mousepos):
        return (self.x <= mousepos[0] and self.x+self.width>=mousepos[0]) and (self.y <= mousepos[1] and self.y+self.height>=mousepos[1])

    def update(self, mousepos, mousebut):
        if (not self.visible):
            return

        if (self.state == 0):
            self.string.color = WHITE
        elif self.state ==2:
            self.string.color = WHITE.lerp(BLACK,0.5)
        else:
            self.string.color = BLACK

        if (Controller.keyboard or Controller.controller):
            self.updateC()
            return
        if(self.state !=2):
            if (self.isInside(mousepos)):

                if (self.state != 1):
                    Sound.playSound("change")
                self.state = 1
            else:
                self.state = 0
        elif mousebut[0] and not self.isInside(mousepos):
            self.state = 0
            Controller.keyboardRedirect=False


        if (self.state != 0 and (mousebut[0])):
            self.activate()

    def updateText(self,u):
        print(u,self.state)
        if not (self.visible and self.state == 2):
            return
        print(u)
        if u == "\r":
            self.state = 0
            Controller.keyboardRedirect=False
        elif u == "\x08":
            self.string.string=self.string.string[:-1]
        elif u.isprintable() and (self.maxwidth<0 or len(self.string.string)<self.maxwidth):
            self.string.string+=u

    def activate(self):
        self.state = 2
        Controller.keyboardRedirect = True

    def updateC(self):
        if(self.state ==2):
            return

        if Controller.menuSelector % self.menuCount == self.id:
            if self.state != 1:
                Sound.playSound("change")
            self.state = 1
        else:
            self.state = 0

        if self.state == 1 and Controller.menuActivate:
            Controller.menuActivate = False
            self.activate()

class Button:
    def __init__(self,string,x,y,width,height,function=None,argument=None,color=WHITE,id=0,menuCount=1,scale=12):
        self.string=StringC(string,x,y,WHITE,scale=scale)
        self.string.x = x+0.5
        self.string.y = y+height-self.string.height

        self.visible=True
        self.color = color
        self.x=x
        self.y=y
        self.width = width
        self.height = height
        self.state=0
        self.function=function
        self.argument=argument
        self.id=id
        self.menuCount=menuCount

    def isInside(self,mousepos):
        return (self.x <= mousepos[0] and self.x+self.width>=mousepos[0]) and (self.y <= mousepos[1] and self.y+self.height>=mousepos[1])

    def update(self,mousepos,mousebut):
        if (not self.visible):
            return

        if(Controller.keyboard or Controller.controller):
            self.updateC()
            return

        if(self.isInside(mousepos)):
            if (self.state != 1):
                Sound.playSound("change")
            self.state=1
        else:
            self.state=0

        if(self.state==0):
            self.string.color=WHITE
        else:
            self.string.color =BLACK

        if (self.state!=0 and (mousebut[0])):
            mousebut[0]=False
            self.activate()

    def activate(self):
        self.state = 0
        Sound.playSound("click")
        if self.function:
            if self.argument:
                self.function(self.argument)
            else:
                self.function()

    def updateC(self):


        if Controller.menuSelector%self.menuCount == self.id:
            if self.state != 1:
                Sound.playSound("change")
            self.state=1
        else:
            self.state = 0

        if self.state == 0:
            self.string.color = WHITE
        else:
            self.string.color = BLACK

        if self.state==1 and Controller.menuActivate:
            Controller.menuActivate = False
            self.activate()
class ValueBar:
    def __init__(self,x,y,width,height,function=None,argument=None,min=0,max=100,color=WHITE):
        self.visible = True
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min =min
        self.max = max
        self.value =min
        self.function = function
        self.argument = argument
    def getValue(self):
        s = self.function(self.argument)
        s = min(self.max,s)
        s = max(self.min,s)
        self.value = s
        return s
    def update(self):
        self.getValue()


class Button:
    def __init__(self,string,x,y,width,height,function=None,argument=None,color=WHITE,id=0,menuCount=1,scale=12):
        self.string=StringC(string,x,y,color,scale=scale)
        self.string.x = x+0.5
        self.string.y = y+height-self.string.height

        self.visible=True
        self.color = color
        self.x=x
        self.y=y
        self.width = width
        self.height = height
        self.state=0
        self.function=function
        self.argument=argument
        self.id=id
        self.menuCount=menuCount

    def isInside(self,mousepos):
        return (self.x <= mousepos[0] and self.x+self.width>=mousepos[0]) and (self.y <= mousepos[1] and self.y+self.height>=mousepos[1])

    def update(self,mousepos,mousebut):
        if (not self.visible):
            return

        if(Controller.keyboard or Controller.controller):
            self.updateC()
            return

        if(self.isInside(mousepos)):
            if (self.state != 1):
                Sound.playSound("change")
            self.state=1
        else:
            self.state=0

        if(self.state==0):
            self.string.color=WHITE
        else:
            self.string.color =BLACK

        if (self.state!=0 and (mousebut[0])):
            mousebut[0]=False
            self.activate()

    def activate(self):
        self.state = 0
        Sound.playSound("click")
        if self.function:
            if self.argument:
                self.function(self.argument)
            else:
                self.function()

    def updateC(self):


        if Controller.menuSelector%self.menuCount == self.id:
            if self.state != 1:
                Sound.playSound("change")
            self.state=1
        else:
            self.state = 0

        if self.state == 0:
            self.string.color =WHITE
        else:
            self.string.color =BLACK

        if self.state==1 and Controller.menuActivate:
            Controller.menuActivate = False
            self.activate()



class ButtonMenu:
        def __init__(self,x,y,width,height,pad,buttons,function=None,scale=12):
            self.buttons=[]
            self.visible = True
            offset=0
            self.buttonC=len(buttons)
            self.pad=pad+height
            self.y=y
            for b in buttons:
                self.buttons.append(Button(b,x,y+offset*self.pad,width,height,id=offset,menuCount=self.buttonC,argument=buttons[b],function=function,scale=scale))
                offset+=1
            pass
        def add(self,n):
            self.buttons.append(n)
            self.buttonC=len(self.buttons);
            offset=0
            for b in self.buttons:
                b.menuCount=self.buttonC
                b.id=offset
                offset += 1

        def update(self, mousepos, mousebut):
            if(not self.visible):
                return

            for b in self.buttons:
                b.update(mousepos,mousebut)


