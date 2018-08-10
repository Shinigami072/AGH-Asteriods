from Screen.Screen import Screen
import View.ScreenRenderer as gui
import Sound

class HiScoreScreen(Screen):

    def __init__(self,hiscores,scale):
        super().__init__("HiScore")
        self.renderer = gui.ScreenRenderer(self.Width ,self.Height )

        menu = gui.ButtonMenu(15, 5, 25, 7, 1, {
            "Main Menu": "Main"
        }, function=self.changeScreen, scale=scale)
        self.guiObjects.append(menu)

        self.hiScoreT=hiscores

        self.hiScores = gui.StringC(hiscores.__str__(),55,5,font="mono-36")
        self.guiObjects.append(self.hiScores)

    def changeTo(self,game):
        self.hiScoreT.write()
        self.hiScores.string=self.hiScoreT.__str__()

        if Sound.musicChannel.get_sound() != Sound.getSound("m_menu"):
            Sound.playMusic("m_menu")


