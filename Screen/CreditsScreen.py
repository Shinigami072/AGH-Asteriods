from Screen.Screen import Screen
import View.ScreenRenderer as gui
import Sound

class CreditsScreen(Screen):

    def __init__(self,scale):
        super().__init__("Credits")
        menu = gui.ButtonMenu(15, 5, 25, 7, 1, {
            "Back": "Main"
        }, function=self.changeScreen, scale=scale)
        self.guiObjects.append(menu)


        F = open("files/Credits", "r")
        print(F)
        self.credits = gui.StringC(F.read(),42,50,font="mono-24")
        F.close()
        self.guiObjects.append(self.credits)

        self.ytrans=5
        self.speed=2


    def changeTo(self,game):
        self.ytrans=5
        if Sound.musicChannel.get_sound() != Sound.getSound("m_menu"):
            Sound.playMusic("m_menu")


    def updateScreen(self,delta):
        self.ytrans-=delta*self.credits.height*self.speed
        self.credits.y=self.ytrans
        super().updateScreen(delta)
