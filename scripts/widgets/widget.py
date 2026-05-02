# Script for the parent class for all widgets
import pygame

pygame.font.init()

# Set the colours for the base widget
DEFAULTCOLOURS = {
    "col1": (50, 50, 50),
    "col2": (100, 100, 100),
    "col3": (255, 255, 255),
    "border": (200, 200, 200),
    "text": (255, 255, 255)
}
BASEFONT = pygame.font.Font(None, 32)

class Widget:
    # Initialise the widget parent class
    def __init__(self, multX=1, multY=1, posX=0, posY=0, width=200, height=100,
                colours=DEFAULTCOLOURS, alpha=255, text="", font=BASEFONT, shadow=False,
                curve=0, border=0, offset=(0, 0), shadowOffset=(0, 0), textOffset=(0, 0),
                textShadowOffset=(-5, 5), textSizeMultiplier=1,
                shadowAlpha=100, visible=True, active=True, textPosition="center", drawBackground=True):
        # Initialize the widget properties
        self.multX = multX
        self.multY = multY
        self.posX = posX
        self.posY = posY    
        self.width = width
        self.height = height
        self.colours = colours
        if "col1" in colours.keys():
            self.colour = colours["col1"]
        else:
            self.colour = (0, 0, 0)
        self.alpha = alpha
        self.text = text
        self.font = font
        self.shadow = shadow
        self.curve = curve
        self.border = border
        self.offset = offset
        self.shadowOffset = shadowOffset
        self.textOffset = textOffset
        self.textShadowOffset = textShadowOffset
        self.textSizeMultiplier = textSizeMultiplier
        self.shadowAlpha = shadowAlpha
        self.visible = visible
        self.active = active
        self.drawBackground = drawBackground
        self.textPosition = textPosition
        # Create extra variables
        self.setInitialSize = False
        self.textObj = self.createTextSurface(self.alpha)
        self.textShadowObj = self.createTextSurface(self.shadowAlpha)
        if self.width == 0 or self.height == 0:
            self.width = self.textObj.get_width()
            self.height = self.textObj.get_height()
        else:
            self.setInitialSize = True
        # Convert a string position into numbers
        self.posX, self.posY = self.StringToNumberPosition(posX, posY)
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.surface = self.createBackgroundSurface(self.alpha)
        self.rectShadow = self.createBackgroundSurface(self.shadowAlpha, shadow=True)
        self.scroll = pygame.Vector2(0, 0)
        self.originalBorder, self.originalCurve = border, curve
        self.updateSize(1, 1, self.multX, self.multY)
        
    # Fucntion to update the position of the widget
    def ChangePosition(self, x, y):
        self.posX, self.posY = self.StringToNumberPosition(x, y)
        self.rect.x = self.posX
        self.rect.y = self.posY
        
    # Function to change a string position into a number and return the values
    def StringToNumberPosition(self, posX, posY):
        # Set local variables to store the new x and y
        x, y = 0, 0
        # Check the type of the positions
        if (type(posX) == int or type(posX) == float):
            x = posX
        else:
            # Convert the strings into lower case
            posX = posX.lower()
        if (type(posY) == int or type(posY) == float):
            y = posY
        else:
            posY = posY.lower()
        # Local variable to store the size of the current window
        win_size = pygame.display.get_window_size()
        # Check what the string is for x
        if posX == "left": x = 0
        elif posX == "right": x = win_size[0]-self.width
        elif posX in ["center", "centre"]: x = win_size[0]/2-self.width/2
        # Check what the string is for y
        if posY == "top": y = 0
        elif posY == "bottom": y = win_size[1]-self.height
        elif posY in ["center", "centre"]: y = win_size[1]/2-self.height/2
        # Return the new position
        return x, y
        
    # Procedure for the child class to add extra update size functionality
    def childUpdateSize(self, oldMultX, oldMultY, multX, multY):
        # Default implementation does nothing
        pass

    # Procedure to update the widget size
    def updateSize(self, oldMultX, oldMultY, multX, multY):
        # Update the widget's position and size based on the new multipliers
        self.multX = multX
        self.multY = multY
        self.rect.x = self.posX * multX
        self.rect.y = self.posY * multY
        self.rect.width = self.width * multX
        self.rect.height = self.height * multY
        self.curve = int(self.originalCurve * ((multX + multY) / 2))
        self.border = int(self.originalBorder * ((multX + multY) / 2))
        self.offset = (((self.offset[0] / oldMultX) * multX), (self.offset[1] / oldMultY) * multY)
        self.shadowOffset = (((self.shadowOffset[0] / oldMultX) * multX), (self.shadowOffset[1] / oldMultY) * multY)
        self.textOffset = (((self.textOffset[0] / oldMultX) * multX), (self.textOffset[1] / oldMultY) * multY)
        self.textShadowOffset = (((self.textShadowOffset[0] / oldMultX) * multX), (self.textShadowOffset[1] / oldMultY) * multY)
        self.textObj = self.createTextSurface(self.alpha)
        self.textShadowObj = self.createTextSurface(self.shadowAlpha)
        self.rectShadow = self.createBackgroundSurface(self.shadowAlpha, shadow=True)
        self.surface = self.createBackgroundSurface(self.alpha)
        self.childUpdateSize(oldMultX, oldMultY, multX, multY)

    # Function to get the position of the text
    def getTextPosition(self, txtObj):
        t = txtObj
        if self.textPosition == "center":
            return (self.rect.centerx-t.get_width()/2, self.rect.centery-t.get_height()/2)
        elif self.textPosition == "left":
            return (self.rect.left + self.textOffset[0], self.rect.centery)
        elif self.textPosition == "right":
            return (self.rect.right - self.textOffset[0], self.rect.centery)
        elif self.textPosition == "top":
            return (self.rect.centerx, self.rect.top + self.textOffset[1])
        elif self.textPosition == "bottom":
            return (self.rect.centerx, self.rect.bottom - self.textOffset[1])
        else:
            return (self.rect.left, self.rect.top)

    # Function to create the text surface
    def createTextSurface(self, alpha, txt=None):
        text = txt if txt is not None else self.text
        # Create the surface
        surf = self.font.render(text, True, self.colours["text"])
        # Set the alpha value
        surf.set_alpha(alpha)
        # Resize the surface
        surf = pygame.transform.scale(surf, (int(surf.get_width() * self.multX * self.textSizeMultiplier), int(surf.get_height() * self.multY * self.textSizeMultiplier)))
        # Return the surface
        return surf.convert_alpha()

    # Function to create a background surface
    def createBackgroundSurface(self, alpha, shadow=False, colour=None):
        # Create the background surface
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # Fill the surface with the background colour
        surf.fill((1, 2, 3))
        # Set a colorkey value to make it transparent
        surf.set_colorkey((1, 2, 3))
        # Set the alpha value
        surf.set_alpha(alpha)
        # Draw a rect
        if colour == None:
            pygame.draw.rect(surf, self.colour, (0, 0, self.rect.width, self.rect.height), 0, self.curve)
        else:
            pygame.draw.rect(surf, colour, (0, 0, self.rect.width, self.rect.height), 0, self.curve)
        # Check if its not a shadow and draw a border on top
        if not shadow and self.border > 0:
            pygame.draw.rect(surf, self.colours["border"], (0, 0, self.rect.width, self.rect.height), self.border, self.curve)
        return surf.convert_alpha()

    # Procedure to update the scroll value of the widget
    def scroll(self, scrollX, scrollY):
        self.scroll.x = scrollX
        self.scroll.y = scrollY

    # Procedure to allow updtating the widget from the child class
    def childUpdate(self):
        # Default implementation does nothing
        pass

    # Procedure to update the widget
    def update(self):
        if self.visible:
            self.childUpdate()

    # Procedure to draw the widget
    def draw(self, screen):
        if not self.visible:
            return
        
        self.rect.x = self.posX * self.multX + self.scroll.x + self.offset[0]
        self.rect.y = self.posY * self.multY + self.scroll.y + self.offset[1]

        # Background
        if self.shadow:
            self.rectShadow = self.createBackgroundSurface(self.shadowAlpha, shadow=True)
            screen.blit(self.rectShadow, (self.rect.x + self.shadowOffset[0],
                                          self.rect.y + self.shadowOffset[1]))
        if self.drawBackground:
            self.surface = self.createBackgroundSurface(self.alpha)
            screen.blit(self.surface, (self.rect.x, self.rect.y)) 

        # Text
        if self.shadow:
            shadowPos = self.getTextPosition(self.textShadowObj)
            screen.blit(self.textShadowObj, (shadowPos[0] + self.textShadowOffset[0] + self.scroll.x,
                                             shadowPos[1] + self.textShadowOffset[1] + self.scroll.y))
        textPos = self.getTextPosition(self.textObj)
        screen.blit(self.textObj, (textPos[0] + self.textOffset[0] + self.scroll.x,
                                   textPos[1] + self.textOffset[1] + self.scroll.y))



