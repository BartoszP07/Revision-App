# Import modules
import pygame
from scripts.widgets import *
from scripts.screens.screen import Screen
from scripts.text_box import Textbox

# Create the class for the start screen and inherit from the main screen class
class SettingsScreen(Screen):
    SCREENW, SCREENH = None, None
    FONT = None
    COLOURS = None
    # Initialise the class
    def __init__(self):
        # Initialise the parent class
        super().__init__()
        self.darken_surf = pygame.Surface((SettingsScreen.SCREENW,
                                           SettingsScreen.SCREENH))
        self.darken_surf.set_alpha(200)
        self.darken_surf = self.darken_surf.convert_alpha()
        self.window_surf = self.CreateAASurf(SettingsScreen.SCREENW*0.9,
                                           SettingsScreen.SCREENH*0.9)
        self.window_surf_position = pygame.Vector2(
            SettingsScreen.SCREENW/2 - self.window_surf.get_width()/2,
            SettingsScreen.SCREENH/2 - self.window_surf.get_height()/2
        )
        
        self.buttons["return"] = Button(posX=100, posY=400, text="Return",
                width=100, height=50, command=self.Return,
                font=SettingsScreen.FONT, textShadowOffset=(-1, 1),
                curve=20)
        self.buttons["save"] = Button(posX=300, posY=400, text="Save",
                width=100, height=50, font=SettingsScreen.FONT,
                textShadowOffset=(-1, 1), curve=20)
        self.exit_settings = False

    def CreateAASurf(self, width, height, alpha=255):
        scale_factor = 4
        border_radius = 20 * scale_factor
        border_weight = 5 * scale_factor
        temp_rect = pygame.Rect(0, 0, width*scale_factor, height*scale_factor)
        temp_surf = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, Textbox.COLOURS["card-background"], temp_rect, 0, border_radius)
        pygame.draw.rect(temp_surf, Textbox.COLOURS["accent"], temp_rect, border_weight, border_radius)
        aa_surf = pygame.transform.smoothscale(temp_surf, (width, height))
        aa_surf.set_alpha(alpha)
        return aa_surf.convert_alpha()

    # Subroutine to exit from the settings
    def Return(self):
        self.exit_settings = True
        
    # Subroutine to update the screen
    def Update(self, delta_time):
        self.UpdateWidgets(delta_time)
        
    # Subroutine to render the screen
    def Render(self, screen):
        screen.blit(self.darken_surf, (0, 0))
        screen.blit(self.window_surf, self.window_surf_position)
        self.RenderWidgets(screen)