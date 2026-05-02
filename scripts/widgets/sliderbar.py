# Import libraries to use
import pygame
# from scripts.globals import *

# Set a class for the silderbar
class Sliderbar:
    # Use a constructor to initalise the class
    def __init__(self, settings,
                x=600,y=300,width=300,height=50,colours=((255,255,255),(255,0,0),(255,255,255)),font=pygame.font.SysFont(None,32),
                label="sliderbar",labelShadow=True,labelPosition="left",labelOffset=(-20,0),
                showValue=True,valueShadow=True,valuePosition="right",valueOffset=(20,0),
                sliderWidth=40,sliderHeight=45,sliderShadow=True,
                sliderbarShadow=True, sliderbarShadowOffset=(-5,5),
                minValue=0,maxValue=100,startValue=50,
                valueShadowOffset=(-3,3), labelShadowOffset=(-3,3),
                sliderShadowOffset=(-3,3), roundTo=0,
                controllerControls={},):
        # Initialise parameter variables
        self.settings = settings
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.colours, self.font = colours, font
        self.label, self.labelShadow, self.labelPosition, self.labelOffset = label, labelShadow, labelPosition, labelOffset
        self.showValue, self.valueShadow, self.valuePosition, self.valueOffset = showValue, valueShadow, valuePosition, valueOffset
        self.sliderWidth, self.sliderHeight, self.sliderShadow = sliderWidth, sliderHeight, sliderShadow
        self.sliderbarShadow, self.sliderbarShadowOffset = sliderbarShadow, sliderbarShadowOffset
        self.minValue, self.maxValue, self.startValue = minValue, maxValue, startValue
        self.valueShadowOffset, self.labelShadowOffset = valueShadowOffset, labelShadowOffset
        self.sliderShadowOffset = sliderShadowOffset
        self.roundTo = roundTo
        self.controllerControls = controllerControls
        # Initialise extra variables
        self.originalPosition = (self.x, self.y)
        self.originalSize = (self.width, self.height)
        self.originalLabelOffset = labelOffset
        self.originalValueOffset = valueOffset
        self.originalSliderSize = (self.sliderWidth, self.sliderHeight)
        self.originalSliderbarShadowOffset = sliderbarShadowOffset
        self.originalValueShadowOffset = valueShadowOffset
        self.originalLabelShadowOffset = labelShadowOffset
        self.originalSliderShadowOffset = sliderShadowOffset
        self.originalValuePosition = valuePosition
        self.originalLabelPosition = labelPosition
        # Alter values to contribute for screen resizing
        self.width *= self.settings["multX"]
        self.height *= self.settings["multY"]
        self.labelOffset = (self.labelOffset[0]*self.settings["multX"], self.labelOffset[1]*self.settings["multY"])
        self.valueOffset = (self.valueOffset[0]*self.settings["multX"], self.valueOffset[1]*self.settings["multY"])
        self.sliderWidth *= self.settings["multX"]
        self.sliderHeight *= self.settings["multY"]
        self.sliderbarShadowOffset = (self.sliderbarShadowOffset[0]*self.settings["multX"], self.sliderbarShadowOffset[1]*self.settings["multY"])
        self.valueShadowOffset = (self.valueShadowOffset[0]*self.settings["multX"], self.valueShadowOffset[1]*self.settings["multY"])
        self.labelShadowOffset = (self.labelShadowOffset[0]*self.settings["multX"], self.labelShadowOffset[1]*self.settings["multY"])
        self.sliderShadowOffset = (self.sliderShadowOffset[0]*self.settings["multX"], self.sliderShadowOffset[1]*self.settings["multY"])
        # Initialise extra values
        self.value = self.startValue
        self.changingValue = False
        self.canClick = False
        self.canPress = False
        self.percentage = 0
        # Initialise the sliderbar rect
        self.sliderRect = pygame.Rect(0, 0, self.sliderWidth, self.sliderHeight)
        self.sliderRectShadow = self.createShadowSurf(100, self.sliderRect, self.colours[1])
        self.rect = pygame.Rect(0, 0, self.width+self.sliderWidth, self.height)
        self.rectShadow = self.createShadowSurf(100, self.rect, self.colours[0])
        # Initialise texts
        self.text = self.createText(255, self.label)
        self.textShadow = self.createText(100, self.label)
        self.valueText = self.createText(255, str(self.value))
        self.valueTextShadow = self.createText(100, str(self.value))
        # Calculate new positions using a subroutine
        if type(self.x) == str: self.x = self.convertAxis(self.x, "x")
        if type(self.y) == str: self.y = self.convertAxis(self.y, "y")
        # Initialise original variables to accomodate for screen resizing
        self.originalPosition = (self.x, self.y)
        self.originalLabelPosition = self.labelPosition
        self.originalValuePosition = self.valuePosition
        # Alter values to contribute for screen resizing
        self.x *= self.settings["multX"]
        self.y *= self.settings["multY"]
        # Update the rect position
        self.rect.x = self.x
        self.rect.y = self.y
        self.sliderRect.x = self.x
        self.sliderRect.y = self.y + abs(self.rect.height - self.sliderRect.height) / 2 # position the slider the middle of the bar
        self.labelPosition = self.convertLabelAxis(self.labelPosition, self.text)
        self.valuePosition = self.convertLabelAxis(self.valuePosition, self.valueText)
        # Calculate the starting position of the sliderRect based on the given starting value
        # Use a vector to store the position of the rect since the position value of a rect is always an integer, resulting to incorrect calculations
        self.sliderRectPos = pygame.math.Vector2(0, 0)
        self.calculateSliderPos()
        
    # Subroutine to calculate the slider position
    def calculateSliderPos(self):
        positionForValue = ((self.value-self.minValue)/(self.maxValue-self.minValue)) * (self.rect.width-self.sliderRect.width)
        self.sliderRectPos.x = positionForValue + self.rect.x
        self.sliderRect.x = self.sliderRectPos.x
        
    # Subroutine to resize the button
    def updateSize(self, settings):
        self.settings = settings
        # Get the new text surface
        self.text = self.createText(255, self.label)
        # Get the new text shadow surface
        self.textShadow = self.createText(100, self.label)
        # Get the new value surface
        self.valueText = self.createText(255, str(self.value))
        # Get the new text shadow surface
        self.valueTextShadow = self.createText(100, str(self.value))
        # Calculate the new slider size
        self.rect.width = self.originalSize[0] * self.settings["multX"]
        self.rect.height = self.originalSize[1] * self.settings["multY"]
        self.sliderRect.width = self.originalSliderSize[0] * self.settings["multX"]
        self.sliderRect.height = self.originalSliderSize[1] * self.settings["multY"]
        # Calculate the new values
        # X and Y
        self.x = self.originalPosition[0] * self.settings["multX"]
        self.y = self.originalPosition[1] * self.settings["multY"]
        # Update rect x and y values
        self.rect.x = self.x
        self.rect.y = self.y
        self.calculateSliderPos()
        self.sliderRect.y = self.y + abs(self.rect.height - self.sliderRect.height) / 2
        # Get new label positions
        self.labelPosition = self.convertLabelAxis(self.originalLabelPosition, self.text)
        self.valuePosition = self.convertLabelAxis(self.originalValuePosition, self.valueText)
        # Get the new sliderbar and sliderrect shadow surfaces
        self.rectShadow = self.createShadowSurf(100, self.rect, self.colours[0])
        self.sliderRectShadow = self.createShadowSurf(100, self.sliderRect, self.colours[1])
        # Offsets
        self.labelOffset = (self.originalLabelOffset[0]*self.settings["multX"], self.originalLabelOffset[1]*self.settings["multY"])
        self.labelShadowOffset = (self.originalLabelShadowOffset[0]*self.settings["multX"], self.originalLabelShadowOffset[1]*self.settings["multY"])
        self.valueOffset = (self.originalValueOffset[0]*self.settings["multX"], self.originalValueOffset[1]*self.settings["multY"])
        self.valueShadowOffset = (self.originalValueShadowOffset[0]*self.settings["multX"], self.originalValueShadowOffset[1]*self.settings["multY"])
        self.sliderShadowOffset = (self.originalSliderShadowOffset[0]*self.settings["multX"], self.originalSliderShadowOffset[1]*self.settings["multY"])
        self.sliderbarShadowOffset = (self.originalSliderbarShadowOffset[0]*self.settings["multX"], self.originalSliderbarShadowOffset[1]*self.settings["multY"])
        
    # Subroutine to convert a string axis to a value
    def convertAxis(self, axisValue, axisType):
        # Check which axis is being affected
        if axisType.lower() == "x":
            # Check which value is to be calculated
            if axisValue.lower() == "center": return (self.settings["windowSize"][0]/2) - (self.rect.width/2)
            elif axisValue.lower() == "left": return 0
            elif axisValue.lower() == "right": return self.settings["windowSize"][0] - self.rect.width
            return 0
        # Check which axis is being affected
        elif axisType.lower() == "y":
            # Check which value is to be calculated
            if axisValue.lower() == "center": return (self.settings["windowSize"][1]/2) - (self.rect.height/2)
            elif axisValue.lower() == "top": return 0
            elif axisValue.lower() == "bottom": return self.settings["windowSize"][1] - self.rect.height
            return 0
    
    # Subroutine to calculate the positions of text based on the position of the sliderbar rect
    def convertLabelAxis(self, axisValue, text):
        # Check which value is to be calculated
        if axisValue == "top": return (self.rect.centerx-text.get_width()/2, self.rect.top - text.get_height())
        elif axisValue == "bottom": return (self.rect.centerx-text.get_width()/2, self.rect.bottom)
        elif axisValue == "left": return (self.rect.left - text.get_width(), self.rect.centery-text.get_height()/2)
        elif axisValue == "right": return (self.rect.right, self.rect.centery-text.get_height()/2)
    
    # Subroutine to create text to be used
    def createText(self, alpha, text):
        # Create the surface for the text
        surf = self.font.render(text, True, self.colours[-1])
        # Resize the surface
        surf = pygame.transform.scale(surf, (surf.get_width()*self.settings["multX"], surf.get_height()*self.settings["multY"]))
        # Set the alpha for the surface
        surf.set_alpha(alpha)
        # Return the surface
        return surf.convert_alpha()
    
    # Subroutine to create shadow surfaces for the rects
    def createShadowSurf(self, alpha, rect, colour):
        # Create the surface for the rect
        surf = pygame.Surface((rect.width, rect.height))
        # Make the background of the surface transparrent
        surf.fill((1,2,4))
        surf.set_colorkey((1,2,4))
        # Draw the rect onto the surface
        pygame.draw.rect(surf, colour, (0,0,rect.width,rect.height))
        # Set the alpha value of the surface
        surf.set_alpha(alpha)
        # Return the surface
        return surf.convert_alpha()
    
    # Subroutine to draw the sliderbar and its components
    def draw(self, screen):
        # Calculate the x and y values for the text
        x = self.labelPosition[0]+self.labelOffset[0]
        y = self.labelPosition[1]+self.labelOffset[1]
        # Calculatte the x and y values for the shadow
        xS = x + self.labelShadowOffset[0]
        yS = y + self.labelShadowOffset[1]
        # Check if the shadow for the text is enabled
        if self.labelShadow:
            # Draw the shadow text on the screen surface
            screen.blit(self.textShadow, (xS, yS))
        # Draw the text on the screen surface
        screen.blit(self.text, (x,y))
            
        # Check if the value should be displayed
        if self.showValue:
            # Calculate the x and y values for the text
            x = self.valuePosition[0]+self.valueOffset[0]
            y = self.valuePosition[1]+self.valueOffset[1]
            # Calculate the x and y values for the text shadow
            xS = x + self.valueShadowOffset[0]
            yS = y + self.valueShadowOffset[1]
            # Check if the shadow for the value should be displayed
            if self.valueShadow:
                # Draw the shadow text on the screen surface
                screen.blit(self.valueTextShadow, (xS,yS))
            # Draw the text on the screen surface
            screen.blit(self.valueText, (x,y))
        
        # Calculate the x and y values for the sliderbar
        # Check if the rect shadow should be displayed
        if self.sliderbarShadow:
            # Calculate the x and y values for the rect shadow
            x = self.rect.x + self.sliderbarShadowOffset[0]
            y = self.rect.y + self.sliderbarShadowOffset[1]
            # Draw the sliderbar shadow
            screen.blit(self.rectShadow, (x, y))
        # Draw the sliderbar rect
        pygame.draw.rect(screen, self.colours[0], self.rect)
        
        # Check if the slider should have a shadow
        if self.sliderShadow:
            # Calculate the x and y for the slider shadow
            x = self.sliderRect.x + self.sliderShadowOffset[0]
            y = self.sliderRect.y + self.sliderShadowOffset[1]
            # Draw the slider shadow
            screen.blit(self.sliderRectShadow, (x, y))
        # Draw the slider onto the screen
        pygame.draw.rect(screen, self.colours[1], self.sliderRect)
        
    # Subroutine to update the sliderbar
    def update(self, settings, mouseRect, controller=None, allowController=False, controllerName=None):
        # Update settings dict
        self.settings = settings
        # Get the mouse buttons list
        mousePressed = pygame.mouse.get_pressed()
        # Check if the controller is allowed and exists and initialise it
        if controller and allowController:
            controllerButton = controller.get_button(self.controllerControls[controllerName]["click"])
        else:
            controllerButton = 0
        
        # Check if the controller is allowed to be used and does exist
        if allowController == False:
            # Check if LMB is not being pressed
            if not mousePressed == (1, 0, 0):
                # Change the value of changing to False
                self.changingValue = False
                # Allow clicking
                self.canClick = True
        else:
            if controller:
                # Check if the controller button is being pressed
                if not controllerButton:
                    # Change the value of changing to False
                    self.changingValue = False
                    # Allow pressing
                    self.canPress = True
                    
        # Check if the sliderbar is colliding with the middle of mouseRect
        if self.rect.collidepoint(mouseRect.center):
            # Check if the controller is allowed to be used and does exist
            if allowController == False:
                # Check if LMB is being pressed
                if mousePressed == (1, 0, 0) and self.canClick:
                    # Set the value of changing to True
                    self.changingValue = True
            else:
                if controller:
                    # Check if the controller button is being pressed
                    if controllerButton and self.canPress:
                        # Set the value of changing to True
                        self.changingValue = True
        
        # Check if the controller is allowed to be used and does exist
        if allowController == False:
            # Check if LMB is being pressed
            if mousePressed == (1, 0, 0):
                # Dont allow clicking
                self.canClick = False
        else:
            if controller:
                # Check if the controller button is being pressed
                if controllerButton:
                    # Dont allow pressing
                    self.canPress = False
            
        # Check if the user is changing the value of the sliderbar
        if self.changingValue:
            # Set the x value of the sliderRect to the x value of the mouseRect
            self.sliderRectPos.x = mouseRect.centerx - self.sliderRect.width / 2
        # Bound the sliderBar between the x and x+width of the sliderbar
        self.sliderRectPos.x = max(self.rect.x, min(self.rect.x+self.rect.width-self.sliderRect.width, self.sliderRectPos.x))
        # Update the position of the sliderRect
        self.sliderRect.x = self.sliderRectPos.x
        
        # Calculate the value of the sliderbar depending on the position of the slider rect
        self.percentage = max(0, min((self.sliderRectPos.x - self.rect.x)/(self.rect.width-self.sliderRect.width), 1))
        self.value = (self.percentage * (self.maxValue-self.minValue)) + self.minValue
        if self.roundTo == 0: self.value = int(self.value)
        else: self.value = round(self.value, self.roundTo)
        
        # Get the surfaces of the value text as the value needs to be updated quite often
        self.valueText = self.createText(255, str(self.value))
        self.valueTextShadow = self.createText(100, str(self.value))
        self.valuePosition = self.convertLabelAxis(self.originalValuePosition, self.valueText)
    
    # Subroutine to return the value of the sliderbar
    def getValue(self):
        # Return value
        return self.value

    # Subroutine to return the percentage of the sliderbar Rect
    def getPercentage(self):
        # Return percentage
        return self.percentage