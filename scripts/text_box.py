# Import libraries
import pygame
from scripts.widgets import *

# Use a class to create the box where the text will be shown
class Textbox:
    SCREENW, SCREENH = None, None
    FONT = None
    COLOURS = None
    # Initialise the class with a constructor
    def __init__(self, width, height):
        # Create the surface
        self.width, self.height = width, height
        self.surf = self.CreateAASurf(width, height)
        self.shadow_surf = self.CreateAASurf(width*1.02, height*1.035, 100)
        self.surf_position = pygame.math.Vector2(
            Textbox.SCREENW/2 - self.surf.get_width()/2,
            Textbox.SCREENH/50
        )
        self.shadow_surf_position = pygame.math.Vector2(
            self.surf_position.x+self.surf.get_width()/2-self.shadow_surf.get_width()/2,
            self.surf_position.y+self.surf.get_height()/2-self.shadow_surf.get_height()/2
        )
        self.text = Text(text="Click To Reveal", font=Textbox.FONT, colours={"text": Textbox.COLOURS["text"]}, shadow=True,
                         textShadowOffset=(-1, 1))

    def CreateAASurf(self, width, height, alpha=255):
        scale_factor = 4
        border_radius = 20 * scale_factor
        border_weight = 10 * scale_factor
        temp_rect = pygame.Rect(0, 0, width*scale_factor, height*scale_factor)
        temp_surf = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, Textbox.COLOURS["card-background"], temp_rect, 0, border_radius)
        pygame.draw.rect(temp_surf, Textbox.COLOURS["accent"], temp_rect, border_weight, border_radius)
        aa_surf = pygame.transform.smoothscale(temp_surf, (width, height))
        aa_surf.set_alpha(alpha)
        return aa_surf.convert_alpha()
        
    # Subroutine to update the colours
    def UpdateColours(self, new_colours):
        Textbox.COLOURS = new_colours
        self.surf = self.CreateAASurf(self.width, self.height)
        self.shadow_surf = self.CreateAASurf(self.width*1.02, self.height*1.035, 100)
        self.text.colours = {"text": Textbox.COLOURS["text"]}
        
    # Update the textbox
    def Update(self):
        self.text.update()
        self.text.ChangePosition(self.surf_position.x+self.surf.get_width()/2-self.text.textObj.get_width()/2,
                                 self.surf_position.y+self.surf.get_height()/2-self.text.textObj.get_height()/2)
    
    # Draw the textbox
    def Draw(self, screen):
        screen.blit(self.shadow_surf, self.shadow_surf_position)
        screen.blit(self.surf, self.surf_position)
        self.text.draw(screen)