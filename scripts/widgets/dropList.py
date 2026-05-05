# Import modules
import pygame

# Use a class to make the droplist
class Droplist:
    # Use a constructor to initialise the class
    def __init__(self, settings, x=0, y=0, width=200, height=75, colours=[(75,75,75), (100,100,100), (50,50,50), (255,255,255)], items=["1","2","3"],
                currentItem=None, maxContent=3, label="droplist", labelPosition="top", labelOffset=(0,0),
                textShadow=True, labelShadow=True, listShadow=True, font=pygame.font.SysFont(None, 32),
                scrollbarWidth=15, command=None, shadowAlpha=100, listShadowOffset=(-5,5),
                textShadowOffset=(-3,3), labelShadowOffset=(-2, 2), curve=10, labelSpacing=20,
                textFont=pygame.font.SysFont(None, 50)):
        # Initialise constructor parameters
        self.settings = settings
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.colours = colours
        self.items, self.currentItem, self.maxContent = items, currentItem, maxContent
        self.label, self.labelPosition, self.labelOffset = label, labelPosition, labelOffset
        self.textShadow, self.labelShadow, self.listShadow = textShadow, labelShadow, listShadow
        self.font, self.textFont = font, textFont
        self.scrollbarWidth = scrollbarWidth
        self.command = command
        self.shadowAlpha, self.listShadowOffset, self.textShadowOffset = shadowAlpha, listShadowOffset, textShadowOffset
        self.labelShadowOffset = labelShadowOffset
        self.curve = curve
        self.labelSpacing = labelSpacing
        # Create "original" variables to compensate for resizing
        self.original = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "scrollbarWidth": scrollbarWidth,
            "labelShadow": labelShadowOffset,
            "textShadow": textShadowOffset,
            "listShadow": listShadowOffset,
        }
        # Resize the variables
        self.x = x * self.settings["multX"]
        self.y = y * self.settings["multY"]
        self.width = width * self.settings["multX"]
        self.height = height * self.settings["multY"]
        self.listShadowOffset = (self.listShadowOffset[0]*self.settings["multX"], self.listShadowOffset[1]*self.settings["multY"])
        self.labelShadowOffset = (self.labelShadowOffset[0]*self.settings["multX"], self.labelShadowOffset[1]*self.settings["multY"])
        self.textShadowOffset = (self.textShadowOffset[0]*self.settings["multX"], self.textShadowOffset[1]*self.settings["multY"])

        # Check if the current item is none
        if self.currentItem == None:
            # Check if the list is larger than 0
            if len(self.items) > 0:
                # Set the current item to be the first in the list
                self.currentItem = self.items[0]

        # Create extra variables to be used
        # Create the current item text
        self.currentItemTxt = self.font.render(str(self.currentItem), True, self.colours[-1])
        # Create a shadow surface for the current item text
        self.currentItemTxtShadow = self.font.render(str(self.currentItem), True, self.colours[-1])
        # Set the alpha of the shadow
        self.currentItemTxtShadow.set_alpha(self.shadowAlpha)
        # Get the max height of the contents displayed
        self.contentHeight = self.height * len(self.items)#self.maxContent
        if self.contentHeight > self.height * self.maxContent:
            self.contentHeight = self.height * self.maxContent
        # Create a surface to display the content
        self.contentSurf = pygame.Surface((self.width, self.contentHeight))
        # Create a shadow for the content
        self.contentSurfShadow = pygame.Surface((self.width, self.contentHeight))
        # Set the alpha for the shadow
        self.contentSurfShadow.set_alpha(self.shadowAlpha)
        # Create a rect to open and close the list
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Create a shadow for the rect
        self.rectShadow = pygame.Surface((self.width, self.height))
        # Set the alpha of the shadow
        self.rectShadow.set_alpha(self.shadowAlpha)
        # Create the label text
        self.text = self.textFont.render(self.label, True, self.colours[-1])
        # Create the label shadow
        self.textShadowSurf = self.text.copy()
        # Set the alpha value
        self.textShadowSurf.set_alpha(self.shadowAlpha)
        # Create text variables to position the text
        self.textX, self.textY = self.calculateTextPosition()
        # Create a flag to determine whether the list is open or closed
        self.isopen = False
        # Create a flag to determine whether the mouse can be clicked
        self.canClick = False
        # Create a list to store all the rects
        self.contentRects = []
        # Create a scroll rect
        self.scrollRect = pygame.Rect(self.x+self.width, self.y+self.height, self.scrollbarWidth, self.height)
        # Create a flag to determine whether the list is being scrolled
        self.scrolling = False
        # Create a variable to get the distance from the topleft of the scroll rect to the mouse position
        self.scrollMouseYDifference = 0
        # Create a variable to calculate the distance the scrollbar needs to travel to show the whole list
        self.travelDistance = (self.height * len(self.items)) - self.contentHeight
        # Create a variable to store the offset y due to the scroll
        self.scrollOffsetY = 0
        # Create a rect for the whole list to determine whether the mouse is colliding with it
        self.collisionRect = pygame.Rect(self.x, self.y, self.width+self.scrollbarWidth,
                                         self.height+self.contentHeight)
        
        # Call the subroutine to create the contents
        self.createContents()

    # Function to darken or light a colour
    def changeBrightness(self, color, factor):
        return tuple(max(0, min(255, int(c * factor))) for c in color)

    # Subroutine to handle scrolling the list using the mouse scroll wheel
    def scrollMouse(self, event, dt, mouseRect):
        # Check whether the mouse is colliding with the list
        if self.collisionRect.colliderect(mouseRect):
            # Move the scroll rect by the y value
            self.scrollRect.y -= (event.precise_y * 5)
        # Confine the scroll rect between 2 y points
        if self.scrollRect.y <= self.y+self.height:
            self.scrollRect.y = self.y+self.height
        elif self.scrollRect.y+self.scrollRect.height >= self.y+self.height+self.contentHeight:
            self.scrollRect.y = self.y+self.contentHeight

    # Subroutine to calculate the text position
    def calculateTextPosition(self):
        # Check each possible position
        if self.labelPosition == "top":
            # Return the position (x, y)
            return (self.rect.centerx-self.text.get_width()/2, self.rect.top-self.text.get_height()/2-(self.labelSpacing*self.settings["multY"]))
        elif self.labelPosition == "bottom":
            # Return the position (x, y)
            return (self.rect.centerx-self.text.get_width()/2, self.rect.bottom+(self.labelSpacing*self.settings["multY"]))
        elif self.labelPosition == "left":
            # Return the position (x, y)
            return (self.rect.left-self.text.get_width()-(self.labelSpacing*self.settings["multX"]), self.rect.centery-self.text.get_height()/2)
        elif self.labelPosition == "right":
            # Return the position (x, y)
            return (self.rect.right+(self.labelSpacing*self.settings["multX"]), self.rect.centery-self.text.get_height()/2)
        # If there are not correct positions, return (0, 0)
        return (0, 0)

    # Subroutine to update sizes
    def updateSize(self, settings):
        # Update the settings dictionary
        self.settings = settings
        # Resize the original variables
        self.x = self.original["x"] * self.settings["multX"]
        self.y = self.original["y"] * self.settings["multY"]
        self.width = self.original["width"] * self.settings["multX"]
        self.height = self.original["height"] * self.settings["multY"]
        self.scrollbarWidth = self.original["scrollbarWidth"] * self.settings["multX"]
        self.listShadowOffset = (self.original["listShadow"][0]*self.settings["multX"],
                                 self.original["listShadow"][1]*self.settings["multY"])
        self.labelShadowOffset = (self.original["labelShadow"][0]*self.settings["multX"],
                                 self.original["labelShadow"][1]*self.settings["multY"])
        self.textShadowOffset = (self.original["textShadow"][0]*self.settings["multX"],
                                 self.original["textShadow"][1]*self.settings["multY"])
        # Create the rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Update the max height
        self.contentHeight = self.height * self.maxContent
        # Create the content surface
        self.contentSurf = pygame.Surface((self.width, self.contentHeight))
        # Create the scrollbar rect
        self.scrollRect = pygame.Rect(self.x+self.width, self.y+self.height, self.scrollbarWidth, self.height)
        # Create the current item text
        self.currentItemTxt = self.font.render(str(self.currentItem), True, self.colours[-1])
        # Resize the text
        self.currentItemTxt = pygame.transform.scale(self.currentItemTxt, (self.currentItemTxt.get_width()*self.settings["multX"],
                                                      self.currentItemTxt.get_height()*self.settings["multY"]))
        # Create a shadow surface for the current item text
        self.currentItemTxtShadow = self.currentItemTxt.copy()
        # Set the alpha of the shadow
        self.currentItemTxtShadow.set_alpha(self.shadowAlpha)
        # Create a shadow for the rect
        self.rectShadow = pygame.Surface((self.width, self.height))
        # Make the shadow transparrent
        self.rectShadow.set_colorkey((1,2,3))
        self.rectShadow.fill((1,2,3))
        # Draw the rect
        pygame.draw.rect(self.rectShadow, self.colours[0], (0, 0, self.width, self.height), 0, self.curve)
        # Set the alpha of the shadow
        self.rectShadow.set_alpha(self.shadowAlpha)
        # Create a shadow for the content
        self.contentSurfShadow = pygame.Surface((self.width, self.contentHeight))
        # Fill the shadow
        self.contentSurfShadow.fill(self.colours[0])
        # Set the alpha for the shadow
        self.contentSurfShadow.set_alpha(self.shadowAlpha)
        # Create the label text
        self.text = self.textFont.render(self.label, True, self.colours[-1])
        # Resize the text
        self.text = pygame.transform.scale(self.text, (self.text.get_width()*self.settings["multX"],
                                                      self.text.get_height()*self.settings["multY"]))
        # Create the label shadow
        self.textShadowSurf = self.text.copy()
        # Set the alpha value
        self.textShadowSurf.set_alpha(self.shadowAlpha)
        # Create all of the item objects
        self.createContents()
        # Create a variable to calculate the distance the scrollbar needs to travel to show the whole list
        self.travelDistance = (self.height * len(self.items)) - self.contentHeight
        # Reset the scroll offset
        self.scrollOffsetY = 0
        # Create text variables to position the text
        self.textX, self.textY = self.calculateTextPosition()
        # Create a rect for the whole list to determine whether the mouse is colliding with it
        self.collisionRect = pygame.Rect(self.x, self.y, self.width+self.scrollbarWidth,
                                         self.height+self.contentHeight)
        
    # Subroutine to create the content surface
    def createContents(self):
        # Clear the list
        self.contentRects = []
        # Make the surface transparrent
        self.contentSurf.fill((1,2,3))
        self.contentSurf.set_colorkey((1,2,3))
        # Loop through each list item
        for idx, item in enumerate(self.items):
            # Calculate the y value
            y = self.height*idx
            # Get the text object
            txt = self.font.render(str(item), True, self.colours[-1])
            # Resize the text
            txt = pygame.transform.scale(txt, (txt.get_width()*self.settings["multX"],
                                          txt.get_height()*self.settings["multY"]))
            # Create a rect for each item
            self.contentRects.append(listItem(self, self.settings, 0, y, self.width, self.height, self.colours, txt, item,
                                              self.labelShadowOffset))

    # Subroutine to update the list
    def update(self, mouseRect):
        self.colours[1] = self.changeBrightness(self.colours[0], 1.2)
        self.colours[2] = self.changeBrightness(self.colours[0], 0.8)
        
        mouseBtn = pygame.mouse.get_pressed() == (1, 0, 0)
        # Check if the mouse buttons is not being pressed
        if not mouseBtn:
            # Set the can click flag to true
            self.canClick = True
            # Set the scrolling flag to false to stop scrolling
            self.scrolling = False

        # Check if the mouse rect is colliding with the list rect
        if self.rect.colliderect(mouseRect):
            # Check if the mouse buttons is being pressed and can be clicked
            if mouseBtn and self.canClick:
                # Toggle the is open flag
                if self.isopen: self.isopen = False
                else: self.isopen = True

        # Check if the mouse rect collides with the scroll rect
        if self.scrollRect.colliderect(mouseRect) and self.canClick and mouseBtn:
            # Calculate the difference in the positions between the mouse and scrollbar
            self.scrollMouseYDifference = self.scrollRect.y - mouseRect.y
            # Set the scroll flag to true
            self.scrolling = True

        # Check if not scrolling
        if not self.scrolling:
            # Check whether if the mouse is not colliding with the list
            if not self.collisionRect.colliderect(mouseRect):
                # Check if the mouse has been clicked
                if mouseBtn and self.canClick:
                    # Close the list
                    self.isopen = False 

        # Check if scrolling
        if self.scrolling:
            # Set the y position of the scrollbar to the position of the mouse
            self.scrollRect.y = mouseRect.y + self.scrollMouseYDifference

        # Confine the scroll rect between 2 y points
        if self.scrollRect.y <= self.y+self.height:
            self.scrollRect.y = self.y+self.height
        elif self.scrollRect.y+self.scrollRect.height >= self.y+self.height+self.contentHeight:
            self.scrollRect.y = self.y+self.contentHeight

        # Get the percentage of how much the scroll rect has moved
        if self.travelDistance > 0:
            scrollPercentage = (self.scrollRect.y-self.rect.y-self.height)/(self.contentHeight-self.height)
            # Calculate the scroll offset y
            self.scrollOffsetY = scrollPercentage * self.travelDistance
            # Confine the offset between 2 values
            if self.scrollOffsetY < 0: self.scrollOffsetY = 0
            elif self.scrollOffsetY > self.travelDistance:
                self.scrollOffsetY = self.travelDistance
        else:
            self.scrollOffsetY = 0

        # Check if the mouse button is being pressed
        if mouseBtn:
            # Set the can click flag to false
            self.canClick = False

        # Check if it is open
        if self.isopen:
            # Loop through each content rect and update it
            for rect in self.contentRects:
                # Update the content rects
                rect.update(mouseRect, self.x, self.y+self.height, self.contentHeight, self.scrollOffsetY, self.scrolling)
        else:
            # Reset the scroll offset to 0
            self.scrollOffsetY = 0
            # Set the position of the scroll bar to its initial position
            self.scrollRect.topleft = (self.x+self.width, self.y+self.height)

        # Update the current item text
        self.currentItemTxt = self.font.render(f"{self.currentItem}", True, self.colours[-1])
        # Resize the text
        self.currentItemTxt = pygame.transform.scale(self.currentItemTxt, (self.currentItemTxt.get_width()*self.settings["multX"],
                                                      self.currentItemTxt.get_height()*self.settings["multY"]))
        # Create a shadow surface for the current item text
        self.currentItemTxtShadow = self.currentItemTxt.copy()
        # Set the alpha of the shadow
        self.currentItemTxtShadow.set_alpha(self.shadowAlpha)

    # Subroutine to draw the list
    def draw(self, screen):
        # Check if the list shadow should be drawn
        if self.listShadow:
            # Make the shadow transparrent
            self.rectShadow.set_colorkey((1,2,3))
            self.rectShadow.fill((1,2,3))
            # Draw the rect
            # Check if the list is open
            if self.isopen:
                pygame.draw.rect(self.rectShadow, self.colours[0], (0, 0, self.width, self.height), 0, 0, self.curve, self.curve)
            else:
                pygame.draw.rect(self.rectShadow, self.colours[0], (0, 0, self.width, self.height), 0, self.curve)
            # Draw the shadow
            screen.blit(self.rectShadow, (self.rect.x+self.listShadowOffset[0], self.rect.y+self.listShadowOffset[1]))
        # Draw the list rect
        pygame.draw.rect(screen, self.colours[0], self.rect, 0, self.curve)
        # Check if the text shadow should be drawn
        if self.labelShadow:
            # Draw the shadow
            screen.blit(self.currentItemTxtShadow, (self.rect.centerx-self.currentItemTxtShadow.get_width()/2+self.labelShadowOffset[0],
                                          self.rect.centery-self.currentItemTxtShadow.get_height()/2+self.labelShadowOffset[1]))
        # Draw the current item text
        screen.blit(self.currentItemTxt, (self.rect.centerx-self.currentItemTxt.get_width()/2,
                                          self.rect.centery-self.currentItemTxt.get_height()/2))
        # Check if the list is open
        if self.isopen:
            # Check if the content shadow should be drawn
            if self.listShadow:
                self.contentSurfShadow.fill(self.colours[0])
                # Set the alpha for the shadow
                self.contentSurfShadow.set_alpha(self.shadowAlpha)
                # Draw the shadow
                screen.blit(self.contentSurfShadow, (self.x+self.listShadowOffset[0], self.y+self.height+self.listShadowOffset[1]))
            # Make the surface transparrent
            self.contentSurf.fill((1,2,3))
            self.contentSurf.set_colorkey((1,2,3))
            # Loop through each content item and draw it to the surface
            for rect in self.contentRects:
                rect.draw(self.contentSurf)
            # Draw the content surface
            screen.blit(self.contentSurf, (self.x, self.y+self.height))
            # Draw the scroll rect
            # Only draw it when there is more than 0 distance to travel
            if self.travelDistance > 0:
                pygame.draw.rect(screen, self.colours[1], self.scrollRect)
            # Draw a border
            borderSize = min(1, max(int(1*((self.settings["multX"]+self.settings["multY"])/2)), 5))
            pygame.draw.rect(screen, self.colours[-1], self.rect, borderSize, 0, self.curve, self.curve)
    
        # Check if the text shadow should be drawn
        if self.textShadow:
            # Draw the text shadow
            screen.blit(self.textShadowSurf, (self.textX+self.textShadowOffset[0], self.textY+self.textShadowOffset[1]))
        # Draw the descriptive text
        screen.blit(self.text, (self.textX, self.textY))

# Use a class to create a list item
class listItem:
    # Use a constructor to initialise the class
    def __init__(self, dList, settings, x, y, width, height, colours, labelObj, item, shadowOffset):
        # Initialise parameter variables
        self.dropList = dList
        self.settings = settings
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colours = colours
        self.currentColour = self.colours[0]
        self.text = labelObj
        self.item = str(item)
        self.shadowOffset = shadowOffset
        # Create the rect for the item
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Create a shadow for the text
        self.textShadowSurf = labelObj.copy()
        # Create extra variables to use
        # Create a flag to detetmine whether the mouse can click
        self.canClick = False
        # Create a flag to determine whether the press colour should be pressed
        self.keepPressColour = False

    # Subroutine to update the item
    def update(self, mouseRect, offsetX, offsetY, updateThreshold, scrollY, isScrolling):
        # Change the position of the rect with the scroll value added
        self.rect.y = self.y - scrollY
        mouseBtn = pygame.mouse.get_pressed() == (1, 0, 0)
        # Check if the mouse button is not pressed
        if not mouseBtn: self.canClick = True
        # Check if the rect is within the threshold
        if -10 <= self.rect.y <= updateThreshold and not isScrolling:
            # Check if the mouse is hovering over the rect
            if self.rect.collidepoint((mouseRect.x-offsetX, mouseRect.y-offsetY)):
                # Set the colour to the hover colour
                self.currentColour = self.colours[1]
                # Check if the mouse button is being pressed
                if mouseBtn and self.canClick:
                    # Set the colour to the press colour
                    self.currentColour = (0, 255, 255)
                    # Set the keep press colour flag to true
                    self.keepPressColour = True
                # Check if the press colour should be kept and the mouse is not being pressed anymore -- confirm the selection
                if self.keepPressColour and not mouseBtn:
                    # Set the current item to this
                    self.dropList.currentItem = self.item
                    # Close the drop list
                    self.dropList.isopen = False
                    # Set the keep press colour to false
                    self.keepPressColour = False
                    # Check if there is a command
                    if self.dropList.command:
                        # Call the command
                        self.dropList.command(self.item)
            else:
                # Set the current colour to the original colour
                self.currentColour = self.colours[0]
                # Check if the mouse button is not being pressed
                if not mouseBtn:
                    # Set the keep press colour flag to false
                    self.keepPressColour = False

        # Check if the press colour should be kept
        if self.keepPressColour:
            # Set the colour to the press colour
            self.currentColour = self.colours[2]

        # Check if the mouse button is pressed
        if mouseBtn: self.canClick = False

        # Set the text shadow surface alpha value to the specified alpha value
        self.textShadowSurf.set_alpha(self.dropList.shadowAlpha)

    # Subroutine to draw the item
    def draw(self, surf):
        # Draw the rect
        pygame.draw.rect(surf, self.currentColour, self.rect)
        # Check if the shadow should be drawn
        if self.dropList.labelShadow:
            # Draw the text shadow
            surf.blit(self.textShadowSurf, (self.rect.centerx - self.text.get_width()/2+self.shadowOffset[0],
                                self.rect.centery - self.text.get_height()/2+self.shadowOffset[1]))
        # Draw the text
        surf.blit(self.text, (self.rect.centerx - self.text.get_width()/2,
                              self.rect.centery - self.text.get_height()/2))
        # Draw a border
        borderSize = min(5, max(int(1*((self.settings["multX"]+self.settings["multY"])/2)), 1))
        pygame.draw.rect(surf, self.colours[-1], self.rect, borderSize)

        
