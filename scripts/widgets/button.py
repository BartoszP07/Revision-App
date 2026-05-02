# Import libraries
import pygame
from scripts.widgets.widget import Widget


# Set the colours for the base widget
DEFAULTCOLOURS = {
    "col1": (150, 0, 0),
    "col2": (100, 100, 100),
    "col3": (255, 255, 255),
    "border": (200, 0, 0),
    "text": (255, 255, 255)
}
BASEFONT = pygame.font.Font(None, 65)

# Create the button class inheriting from Widget
class Button(Widget):
    # Initialise the button class
    def __init__(self, multX=1, multY=1, posX=100, posY=100, width=350, height=100,
                 colours=None, alpha=255, text="Button", font=None, shadow=True,
                 curve=0, border=0, offset=(0, 0), shadowOffset=(-3, 3), textOffset=(0, 0),
                 textShadowOffset=(-5, 5), textSizeMultiplier=1, prioritiseSprite=True,
                 shadowAlpha=100, visible=True, active=True, textPosition="center", drawBackground=True,
                 command=None, parameters=None, pressSound=None, sprite=None):
        if colours is None:
            colours = DEFAULTCOLOURS
        if font is None:
            font = BASEFONT
        super().__init__(multX, multY, posX, posY, width, height,
                         colours, alpha, text, font, shadow,
                         curve, border, offset, shadowOffset,
                         textOffset, textShadowOffset, textSizeMultiplier,
                         sprite, shadowAlpha, visible,
                         active, textPosition, drawBackground)
        
        self.command = command
        self.parameters = parameters
        self.pressSound = pressSound
        self.colliding = False
        self.canPress = False
        self.keepPressColour = False
        self.didKeepPressColour = False
        self.highlighted = False
        self.prioritiseSprite = prioritiseSprite
        self.sprite = sprite
        if self.sprite:
            self.spriteAlphaSurf = pygame.mask.from_surface(self.sprite)
            if self.prioritiseSprite:
                self.width = self.sprite.get_width()
                self.height = self.sprite.get_height()
                self.rect.width = self.width
                self.rect.height = self.height
                self.updateSize(1, 1, 1, 1)
            
        
    # Procedure to change the text
    def changeText(self, text):
        self.text = text
        self.textObj = self.createTextSurface(self.alpha)
        self.textShadowObj = self.createTextSurface(self.shadowAlpha)
        if self.width == 0 or self.height == 0:
            self.rect = pygame.Rect(self.posX, self.posY, self.textObj.get_width(), self.textObj.get_height())
        else:
            self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.surface = self.createBackgroundSurface(self.alpha)
        self.rectShadow = self.createBackgroundSurface(self.shadowAlpha, shadow=True)
        
    # Function to darken or light a colour
    def changeBrightness(self, color, factor):
        return tuple(max(0, min(255, int(c * factor))) for c in color)

    # Procedure to handle the button click
    def handleClick(self):
        # Check for command
        if self.command:
            if self.parameters:
                # Call the command with parameters
                self.command(*self.parameters)
            else:
                # Call the command without parameters
                self.command()
        # Play the press sound if it exists
        if self.pressSound:
            self.pressSound.play()

    # Procedure to update the button if its a regular rect
    def UpdateRectColours(self, pressing):
         # Check if the rect is colliding
        if self.colliding or self.highlighted:
            self.colour = self.changeBrightness(self.colours["col1"], 1.2)
            if pressing and self.canPress:
                self.colour = self.changeBrightness(self.colours["col1"], 0.8)
                self.keepPressColour = True
                self.didKeepPressColour = True
        else:
            self.colour = self.colours["col1"]
        
        # Keep the press colour if the button is pressed, even if not colliding
        if self.keepPressColour and pressing:
            self.colour = self.changeBrightness(self.colours["col1"], 0.8)

    # Procedure to update the button if its a sprite
    def UpdateSpriteColours(self, pressing):
        # Check if the rect is colliding
        if self.colliding or self.highlighted:
            # Make the sprite brighter
            self.black_sprite.set_alpha(0)
            self.white_sprite.set_alpha(100)
            if pressing and self.canPress:
                self.white_sprite.set_alpha(0)
                self.black_sprite.set_alpha(100)
                self.keepPressColour = True
                self.didKeepPressColour = True
        else:
            self.black_sprite.set_alpha(0)
            self.white_sprite.set_alpha(0)
        
        if self.keepPressColour and pressing:
            self.black_sprite.set_alpha(100)
            self.white_sprite.set_alpha(0)

    # Procedure to update the button -- override the parent class method
    def update(self, rects, pressing):
        if not self.visible: return
        self.colliding = False
        for rect in rects:
            if self.rect.colliderect(rect):
                self.colliding = True
                break
        
        # Check if the button is not pressed
        if not pressing:
            self.canPress = True
            self.keepPressColour = False
       
        if self.sprite:
            self.UpdateSpriteColours(pressing)
        else:
            self.UpdateRectColours(pressing)

        # Check if the mouse has been released
        if not self.keepPressColour and self.didKeepPressColour:
            self.didKeepPressColour = False
            # Only click the button if it is still colliding
            if self.colliding:
                self.handleClick()

        if pressing:
            self.canPress = False