# Import modules
import pygame, sys, time
from scripts import *
from scripts.screens import *

class App:
    def __init__(self):
        # Initialise the data handler
        self.data_handler = DataHandler()
        # Load colours to be used
        self.colours = self.data_handler.LoadJSON("data/colours.json")
        screenW, screenH = 500, 500
        self.screen = pygame.display.set_mode((screenW, screenH))
        pygame.display.set_caption("Revision")
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.font = pygame.font.Font("assets/fonts/PixelCode-Light.ttf", 20)
        self.small_font = pygame.font.Font("assets/fonts/PixelCode-Light.ttf", 15)
        # Load assets to be used -- screen needs to be initialised first !
        self.assets = self.data_handler.LoadAssets("assets")
        
        # Update class global variables
        Textbox.SCREENH = screenH
        Textbox.SCREENW = screenW
        Textbox.FONT = self.font
        Textbox.COLOURS = self.colours
        UserInterface.SCREENW = screenW
        UserInterface.SCREENH = screenH
        UserInterface.FONT = self.font
        UserInterface.ASSETS = self.assets
        UserInterface.COLOURS = self.colours
        SettingsScreen.SMALLFONT = self.small_font
        
        self.ui = UserInterface()
        
    def QuitGame(self):
        pygame.quit()
        sys.exit()
        
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.QuitGame()
    
    def Update(self):
        self.ui.Update(self.delta_time)
        self.ui.text_box.UpdateColours()
        
        # Check if the settings should be saved
        if self.ui.settings_screen.save_settings:
            self.ui.settings_screen.save_settings = False
            self.data_handler.SaveJSON("data/colours.json", self.colours)
            
    
    def Draw(self):
        self.screen.fill(self.colours["background"])
        self.ui.Render(self.screen)
        
    def Run(self):
        while True:
            self.delta_time = self.clock.tick(0) / 1000
            
            self.Events()
            self.Update()
            self.Draw()
            
            pygame.display.flip()
        
    
if __name__ == "__main__":
    a = App()
    a.Run()