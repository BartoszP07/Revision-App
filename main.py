# Import modules
import pygame, sys, time
from scripts import *

class App:
    def __init__(self):
        screenW, screenH = 500, 500
        self.screen = pygame.display.set_mode((screenW, screenH))
        pygame.display.set_caption("Revision")
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.font = pygame.font.Font("assets/PixelCode-Light.ttf", 20)
        
        Textbox.SCREENW = screenW
        Textbox.SCREENH = screenH
        Textbox.FONT = self.font
        self.text_box = Textbox(screenW*0.96, screenH*0.5)
        
        
    def QuitGame(self):
        pygame.quit()
        sys.exit()
        
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.QuitGame()
    
    def Update(self):
        self.text_box.Update()
    
    def Draw(self):
        self.screen.fill((200, 200, 200))
        self.text_box.Draw(self.screen)
        
    def Run(self):
        while True:
            self.delta_time = self.clock.tick(60) / 1000
            
            self.Events()
            self.Update()
            self.Draw()
            
            pygame.display.flip()
        
    
if __name__ == "__main__":
    a = App()
    a.Run()