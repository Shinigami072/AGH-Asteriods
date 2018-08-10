from Screen.Screen import *
import View.ScreenRenderer as gui
import Sound
import Files

class MainScreen(Screen):

    def __init__(self,scale):
        super().__init__("Main")
        self.useRenderer=False
        self.renderer = gui.ScreenRenderer(self.Width , self.Height)

        menu = gui.ButtonMenu(15,5,25,7,1,{
            "Play":"Game",
            "Options":"Option",
            #"Modeling": "model",
            "High Scores":"HiScore",
            "Credits":"Credits",
            "Quit":"QUIT"
        },function=self.changeScreen,scale=scale)

        self.guiObjects.append(menu)

        Sound.playMusic("m_menu")

    def changeTo(self,game):
        if Sound.musicChannel.get_sound() != Files.getSound("m_menu"):
          Sound.playMusic("m_menu")
