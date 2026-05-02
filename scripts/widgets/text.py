# Import libraries
import pygame
from scripts.widgets.widget import Widget

# Set the default font
DEFAULTCOLOURS = {
    "col1": (50, 50, 50),
    "col2": (100, 100, 100),
    "col3": (255, 255, 255),
    "border": (255, 255, 255),
    "text": (255, 255, 255)
}
BASEFONT = pygame.font.Font(None, 32)

# Use a class to make the text widget
class Text(Widget):
    # Initialise the text widget
    def __init__(self, multX=1, multY=1, posX=0, posY=0, width=0, height=0,
                 colours=None, alpha=255, text="Text", font=None, shadow=False,
                 curve=0, border=0, offset=(0, 0), shadowOffset=(0, 0), textOffset=(0, 0),
                 textShadowOffset=(-5, 5), textSizeMultiplier=1,
                 shadowAlpha=100, visible=True, textPosition=None, drawBackground=False,
                 backgroundShadow=False, backgroundShadowOffset=(12, -12), backgroundShadowAlpha=150,
                 backgroundColour=(0,0,0)):
        if colours is None:
            colours = DEFAULTCOLOURS
        if font is None:
            font = BASEFONT
        super().__init__(multX, multY, posX, posY, width, height,
                         colours, alpha, text, font, shadow,
                         curve, border, offset, shadowOffset,
                         textOffset, textShadowOffset, textSizeMultiplier, None,
                         shadowAlpha, visible, True, textPosition, drawBackground)
        
        self.textObjs = []
        self.textLineSpacing = 5
        self.backgroundShadowOffset = backgroundShadowOffset
        self.backgroundShadowAlpha = backgroundShadowAlpha
        self.backgroundShadow = backgroundShadow
        self.backgroundColour = backgroundColour

    # Procedure to change the text
    def changeText(self, text):
        self.text = text
        self.textObj = self.createTextSurface(self.alpha)
        self.textShadowObj = self.createTextSurface(self.shadowAlpha)
        if not self.setInitialSize:
            self.width = self.textObj.get_width()
            self.height = self.textObj.get_height()
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.surface = self.createBackgroundSurface(self.alpha)
        self.rectShadow = self.createBackgroundSurface(self.backgroundShadowAlpha, shadow=True)
    
    # Procedure to update the text
    def childUpdate(self):
        self.textObjs = []
        # Check if the \n is in the text
        if "\n" in self.text:
            # Split the text into lines
            lines = self.text.split("\n")
            for line in lines:
                self.textObjs.append((self.createTextSurface(self.alpha, line), self.createTextSurface(self.shadowAlpha, line)))

    # Procedure to draw the text - overrides the parent class draw method
    def draw(self, screen):
        backgroundTextOffset = (0, 0)
        # Check if a background should be drawn
        if self.drawBackground:
            backgroundTextOffset = (self.width/2 - self.textObj.get_width()/2, self.height/2 - self.textObj.get_height()/2)
            if self.backgroundShadow:
                screen.blit(self.rectShadow, (self.rect.x - self.backgroundShadowOffset[0], self.rect.y - self.backgroundShadowOffset[1]))
            screen.blit(self.surface, (self.rect.x, self.rect.y))
            if self.border:
                pygame.draw.rect(screen, (255, 255, 255), self.rect, self.border, self.curve)
        # Check if there are mutliple text objects
        if len(self.textObjs) == 0:
            # Draw the single text object
            if self.shadow:
                screen.blit(self.textShadowObj, (self.rect.x + self.textShadowOffset[0] + self.scroll.x + backgroundTextOffset[0],
                                                  self.rect.y + self.textShadowOffset[1] + self.scroll.y + backgroundTextOffset[1]))
            screen.blit(self.textObj, (self.rect.x + self.textOffset[0] + self.scroll.x + backgroundTextOffset[0],
                                       self.rect.y + self.textOffset[1] + self.scroll.y + backgroundTextOffset[1]))
            return
        # Loop through the text objects and draw them
        for i, (textObj, textShadowObj) in enumerate(self.textObjs):
            # Draw the shadow
            if self.shadow:
                screen.blit(textShadowObj, (self.rect.x + self.textShadowOffset[0] + self.scroll.x,
                                             self.rect.y + self.textShadowOffset[1] + self.scroll.y + (i * textObj.get_height()) + (i * self.textLineSpacing*self.multY)))
            # Draw the text
            screen.blit(textObj, (self.rect.x + self.textOffset[0] + self.scroll.x,
                                  self.rect.y + self.textOffset[1] + self.scroll.y + (i * textObj.get_height()) + (i * self.textLineSpacing*self.multY)))
