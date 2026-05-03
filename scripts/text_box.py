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
        self.surf_rect = self.surf.get_rect()
        self.surf_rect.topleft = self.surf_position
        self.shadow_surf_position = pygame.math.Vector2(
            self.surf_position.x+self.surf.get_width()/2-self.shadow_surf.get_width()/2,
            self.surf_position.y+self.surf.get_height()/2-self.shadow_surf.get_height()/2
        )
        
        self.texts = {}
        self.texts["reveal"] = Text(text="Click To Flip", font=Textbox.FONT, colours={"text": Textbox.COLOURS["text"]}, shadow=True,
                         textShadowOffset=(-1, 1))
        self.texts["question"] = Text(text="Question", font=Textbox.FONT, colours={"text": Textbox.COLOURS["text"]}, shadow=True,
                         textShadowOffset=(-1, 1))
        self.texts["answer"] = Text(text="Answer", font=Textbox.FONT, colours={"text": Textbox.COLOURS["text"]}, shadow=True,
                         textShadowOffset=(-1, 1))
        
        self.can_click = False
        self.card_side = "question"
        self.question_txt = "q"
        self.answer_txt = "a"

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
    def UpdateColours(self):
        self.surf = self.CreateAASurf(self.width, self.height)
        self.shadow_surf = self.CreateAASurf(self.width*1.02, self.height*1.035, 100)
        for txt in self.texts.values():
            txt.colours = {"text": Textbox.COLOURS["text"]}
        
    # Update the textbox
    def Update(self):
        for key, txt in self.texts.items():
            txt.changeText(txt.text)
            if key in ["answer", "question"]:
                max_width = self.surf.get_width() - 50
                
                # Check if the text actually exceeds the max width in pixels
                if txt.font.size(txt.text)[0] > max_width:
                    
                    # Remove any existing newlines to prevent weird double-spacing, then split into words
                    words = txt.text.replace('\n', ' ').split(' ')
                    lines = []
                    current_line = []
                    
                    for word in words:
                        # See what the line WOULD look like with this next word added
                        test_line = " ".join(current_line + [word])
                        
                        # txt.font.size() returns a tuple: (width, height)
                        # We check the width ([0]) against our max_width
                        if txt.font.size(test_line)[0] <= max_width:
                            current_line.append(word)
                        else:
                            # It's too long! Save the current line, and start a new line with this word
                            lines.append(" ".join(current_line))
                            current_line = [word]
                    
                    # Don't forget to add the very last line
                    if current_line:
                        lines.append(" ".join(current_line))
                    
                    # Stitch it all back together with the \n character
                    wrapped_text = "\n".join(lines)
                    
                    # Apply it to the widget
                    txt.changeText(wrapped_text)
            txt.update()
            
            txt.ChangePosition(
                self.surf_position.x+self.surf.get_width()/2-txt.totalTextWidth/2,
                self.surf_position.y+self.surf.get_height()/2-txt.totalTextHeight/2
            )
        
        self.texts["reveal"].ChangePosition(self.surf_position.x+self.surf.get_width()/2-self.texts["reveal"].textObj.get_width()/2,
                                 self.surf_position.y+self.surf.get_height()/2-self.texts["reveal"].textObj.get_height()/2+
                                 self.surf.get_height()*0.4)
        self.texts["answer"].changeText(self.answer_txt)
        self.texts["question"].changeText(self.question_txt)
        
        
        
        
        mouse_press = pygame.mouse.get_pressed() == (1, 0, 0)
        
        if not mouse_press:
            self.can_click = True
            
        if self.surf_rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_press and self.can_click:
                if self.card_side == "question":
                    self.card_side = "answer"
                else:
                    self.card_side = "question"
        
        if mouse_press:
            self.can_click = False
    
    # Draw the textbox
    def Draw(self, screen):
        screen.blit(self.shadow_surf, self.shadow_surf_position)
        screen.blit(self.surf, self.surf_position)
        for key, txt in self.texts.items():
            if self.card_side == "question":
                if key in ["reveal", "question"]:
                    txt.draw(screen)
            elif self.card_side == "answer":
                if key in ["answer"]:
                    txt.draw(screen)