from Screen.Screen import *
import View.ScreenRenderer as gui
import Sound
import Files
class OptionScreen(Screen):

    def __init__(self,scale):
        super().__init__("Option")
        self.useRenderer=False
        self.renderer = gui.ScreenRenderer(self.Width , self.Height)

        menu = gui.ButtonMenu(15,5,25,7,1,{
            "Volume Sound   +": "_S+",
            "Volume Sound   -": "_S-",
            "Volume Music   +": "_M+",
            "Volume Music   -": "_M-",
            "Return":"Main",
        },function=self.options,scale=scale)

        self.guiObjects.append(menu)
        self.guiObjects.append(gui.ValueBar(50,9,100,7,function=self.getValue,argument="sv"))
        self.guiObjects.append(gui.ValueBar(50,25,100,7,function=self.getValue,argument="mv"))



    def changeScreen(self,name=None):
        Files.writeOptions()

        super().changeScreen(name)
    def getValue(self, value):
        if(value == "sv"):
            return Sound.soundVolume
        if (value == "mv"):
            return Sound.musicVolume
        print(value)
        return 30
    def options(self,option):
        if(option[0]=="_"):
            if(option =="_S+"):
                Sound.soundVolume+=2.5
            if (option == "_S-"):
                Sound.soundVolume -=2.5

            if (option == "_M+"):
                Sound.musicVolume += 2.5
            if (option == "_M-"):
                Sound.musicVolume -= 2.5
        else:
            self.changeScreen(option)
        Sound.setVolume()
        if (Sound.soundVolume < 0):
            Sound.soundVolume = 0
        if (Sound.soundVolume > 100):
            Sound.soundVolume = 100

        if (Sound.musicVolume < 0):
            Sound.musicVolume= 0
        if (Sound.musicVolume > 100):
            Sound.musicVolume = 100
    def changeTo(self,game):
        print("Chaneg")
        Files.readOptions()
        print("reading options")

        if Sound.musicChannel.get_sound() != Files.getSound("m_menu"):
          Sound.playMusic("m_menu")

