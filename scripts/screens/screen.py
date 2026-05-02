# Import modules
import pygame

# Create a parent class for all screens to inherit from
class Screen:
    # Initialise the class
    def __init__(self):
        # Create all neccessary variables for widgets
        self.buttons = {}
        self.texts = {}
        # Create variable to use to see if the first frame of the screen has loaded
        self.has_loaded = False
        # Create a rect for the mouse
        self.mouse = pygame.Rect(0, 0, 1, 1)
        
    # Subroutine to update the widgets
    def UpdateWidgets(self, delta_time):
        # Update the position of the mouse rect to the position of the mouse
        self.mouse.topleft = pygame.mouse.get_pos()
        # Loop through each widget and update them
        for btn in self.buttons.values():
            btn.update([self.mouse], pygame.mouse.get_pressed() == (1, 0, 0))
        for txt in self.texts.values():
            txt.update()
        
    # Subroutine to render the widgets
    def RenderWidgets(self, screen):
        # Loop through each widget and render them
        for btn in self.buttons.values():
            btn.draw(screen)
        for txt in self.texts.values():
            txt.draw(screen)