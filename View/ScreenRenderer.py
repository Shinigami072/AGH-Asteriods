import View.Renderer
from Screen.GUI import *

class ScreenRenderer(View.Renderer.Renderer):
    def __init__(self,width,height):
        super().__init__(width,height)

    def renderString(self,string):
        dy =0 #przesunięcie
        self.font = Files.FONTS[string.font] #wybrany font
        for strin in string.string.splitlines():
            if(len(strin.strip()) >0):#sprawdzenie pustości
                self.screen.blit(self.font.render(strin, True,#wyrenderowanie stringa
                        string.color if strin.strip()[0]!='#' else View.Renderer.DEBUG_PURPLE),
                        (self.getMP(string.x), self.getMP(string.y+dy)))
            dy+=string.height
    def renderButton(self,button):
        width =0
        if(button.state==0):
            width=3 #ustawienie wypełnienia
        pygame.draw.rect(self.screen,
                         button.color,
                         pygame.Rect(self.getMP(button.x),self.getMP(button.y),self.getMP(button.width),self.getMP(button.height)), width
                         )

        self.renderString(button.string)#wyrenderowanie wewnętrznego stirnga

    def renderButtons(self,buttonmenu):#renderowanie
        for b in buttonmenu.buttons:
            self.renderButton(b)

    def renderValueBar(self, valuebar):
        #obramówka
        pygame.draw.rect(self.screen,
                         valuebar.color,
                         pygame.Rect(self.getMP(valuebar.x), self.getMP(valuebar.y), self.getMP(valuebar.width),
                                     self.getMP(valuebar.height)), 3
                         )
        #wypełnienie
        pygame.draw.rect(self.screen,
                         valuebar.color,
                         pygame.Rect(self.getMP(valuebar.x), self.getMP(valuebar.y), self.getMP(valuebar.width*(valuebar.value/valuebar.max)),
                                     self.getMP(valuebar.height)), 0
                         )
    def render(self,guiObjects,delta):
        self.font = Files.FONTS["default"]

        for guiEl in guiObjects:
            if(not guiEl.visible):
                continue
            if( isinstance(guiEl,StringC)):
                self.renderString(guiEl)
            if (isinstance(guiEl, Button)):
                self.renderButton(guiEl)
            if (isinstance(guiEl, Input)):
                self.renderButton(guiEl)
            if (isinstance(guiEl, ButtonMenu)):
                self.renderButtons(guiEl)
            if (isinstance(guiEl, ValueBar)):
                self.renderValueBar(guiEl)
