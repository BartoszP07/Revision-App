# Import modules
import pygame
from scripts.widgets import *
from scripts.screens import *
from scripts.text_box import Textbox

# Create the class for the start screen and inherit from the main screen class
class UserInterface(Screen):
    SCREENW, SCREENH = None, None
    FONT = None
    COLOURS = None
    ASSETS = None
    # Initialise the class
    def __init__(self):
        # Initialise the parent class
        super().__init__()
        self.text_box = Textbox(UserInterface.SCREENW*0.96, UserInterface.SCREENH*0.5)
        
        self.buttons["settings"] = Button(
            sprite=UserInterface.ASSETS["settings-icon"], drawBackground=False,
            text="", posX=UserInterface.SCREENW*0.005, posY=UserInterface.SCREENH*0.93,
            command=self.ShowSettings)
        
        self.buttons["previous"] = Button(
            posX=UserInterface.SCREENW*0.02, posY=UserInterface.SCREENH*0.55,
            width=120, height=25, font=UserInterface.FONT, text="Previous",
            curve=15, textShadowOffset=(-1, 1)
        )
        
        self.buttons["next"] = Button(
            posX=UserInterface.SCREENW*0.74, posY=UserInterface.SCREENH*0.55,
            width=120, height=25, font=UserInterface.FONT, text="Next",
            curve=15, textShadowOffset=(-1, 1)
        )
        
        self.in_settings = False
        
        SettingsScreen.SCREENW = UserInterface.SCREENW
        SettingsScreen.SCREENH = UserInterface.SCREENH
        SettingsScreen.FONT = UserInterface.FONT
        SettingsScreen.COLOURS = UserInterface.COLOURS
        self.settings_screen = SettingsScreen()

    # Subroutine to show the settings
    def ShowSettings(self):
        self.in_settings = True
        
    # Subroutine to update the screen
    def Update(self, delta_time):
        for btn in self.buttons.values():
            btn.colours["col1"] = UserInterface.COLOURS["accent"]
        if not self.in_settings:
            self.UpdateWidgets(delta_time)
            self.text_box.Update()
        else:
            self.settings_screen.Update(delta_time)
        
        if self.settings_screen.exit_settings == True and self.in_settings:
            self.in_settings = False
            self.settings_screen.exit_settings = False
        
    # Subroutine to render the screen
    def Render(self, screen):
        self.text_box.Draw(screen)
        self.RenderWidgets(screen)
        
        if self.in_settings:
            self.settings_screen.Render(screen)