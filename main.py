#! /usr/bin/python3
from Screen.GameScreen import *
from Screen.MainScreen import *


class App:
    def __init__(self):
        print("constructor")
        self.size = self.width, self.height = 1280,720
        self.screen = None;
        self.done = False
        self.current_screen = None
        self.next_screen = None
        self.init()

    def init(self):
        print("Game init")
        pygame.init()
        if(pygame.joystick.get_count() >0):
            pygame.joystick.Joystick(0).init();
        self.clock = pygame.time.Clock()
        self.screen =pygame.display.set_mode(self.size)
        self.done = False
        if (not "Main" in Screen.screenDict.keys()):
            self.current_screen = MainScreen(self)
        else:
            self.current_screen = Screen.screenDict["Main"]

        if (not "Start" in Screen.screenDict.keys()):
            GameScreen(self)

        self.current_screen = Screen.screenDict["Start"]

        self.next_screen = None
        return True

    def cleanup(self):
        print("Cleanup")
        pygame.quit()

    def main(self):
        print("main-func")
        if not self.init():
            self.done = True

        while not self.done:
            if(self.next_screen != None):
                self.current_screen=self.next_screen
                self.next_screen = None

            delta = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    self.done = True
                self.current_screen.handleEvent(event)

            self.screen.fill((0,0,0))
            self.current_screen.updateScreen(delta)
            self.current_screen.renderScreen(self.screen,delta)
            pygame.display.flip()

        self.cleanup()


#Start App
if __name__ =="__main__":
    app = App()
    app.main()