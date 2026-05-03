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
    SMALLFONT = None
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
        
        self.changed_colours = {"background": SettingsScreen.COLOURS["background"]}
        self.current_colour = "background"
        self.colour_preview_rect = pygame.Rect(
            self.window_surf_position.x+self.window_surf.get_width()/2-50,
            self.window_surf_position.y+50,
            100, 100
        )
        
        btnCols = {
            "col1": SettingsScreen.COLOURS["accent"],
            "col2": (100, 100, 100),
            "col3": (255, 255, 255),
            "border": (200, 0, 0),
            "text": (255, 255, 255)
        }
        
        self.buttons["return"] = Button(posX=100, posY=400, text="Return",
                width=100, height=35, command=self.Return,
                font=SettingsScreen.FONT, textShadowOffset=(-1, 1),
                curve=20, colours=btnCols)
        self.buttons["save"] = Button(posX=300, posY=400, text="Save",
                width=100, height=35, font=SettingsScreen.FONT,
                textShadowOffset=(-1, 1), curve=20,
                command=self.SaveColours, colours=btnCols)
        
        btn_w = 90
        btn_h = 25
        btn_y = 200
        pad_x = 15
        total_w = btn_w*4 + pad_x*3
        btn_x = self.window_surf_position.x+self.window_surf.get_width()/2\
            -total_w/2
        self.buttons["background"] = Button(width=btn_w, height=btn_h,
            posX=btn_x+btn_w*0+pad_x*0, font=SettingsScreen.SMALLFONT, text="bg",
            posY=btn_y, textShadowOffset=(-1, 1), curve=15, command=self.ChangeColour,
            parameters=["background"], colours=btnCols)
        self.buttons["card-background"] = Button(width=btn_w, height=btn_h,
            posX=btn_x+btn_w*1+pad_x*1, font=SettingsScreen.SMALLFONT, text="card bg",
            posY=btn_y, textShadowOffset=(-1, 1), curve=15, command=self.ChangeColour,
            parameters=["card-background"], colours=btnCols)
        self.buttons["text"] = Button(width=btn_w, height=btn_h,
            posX=btn_x+btn_w*2+pad_x*2, font=SettingsScreen.SMALLFONT, text="text",
            posY=btn_y, textShadowOffset=(-1, 1), curve=15, command=self.ChangeColour,
            parameters=["text"], colours=btnCols)
        self.buttons["accent"] = Button(width=btn_w, height=btn_h,
            posX=btn_x+btn_w*3+pad_x*3, font=SettingsScreen.SMALLFONT, text="accent",
            posY=btn_y, textShadowOffset=(-1, 1), curve=15, command=self.ChangeColour,
            parameters=["accent"], colours=btnCols)
        
        sliderStartY = 240
        sliderSpacing = 10
        sliderbarX = self.window_surf_position.x+self.window_surf.get_width()/2-100
        self.sliderbars["red"] = Sliderbar(
            {"multX": 1, "multY": 1}, sliderbarX, sliderStartY+30*0+sliderSpacing*0,
            200, 30, font=SettingsScreen.FONT, minValue=0, maxValue=255,
            label="red", sliderHeight=30, startValue=SettingsScreen.COLOURS["background"][0],
            sliderWidth=10, labelShadowOffset=(-1, 1), valueShadowOffset=(-1, 1),
            sliderShadowOffset=(-2, 2), sliderbarShadowOffset=(-2, 2))
        
        self.sliderbars["green"] = Sliderbar(
            {"multX": 1, "multY": 1}, sliderbarX, sliderStartY+30*1+sliderSpacing*1,
            200, 30, font=SettingsScreen.FONT, minValue=0, maxValue=255,
            label="green", sliderHeight=30, startValue=SettingsScreen.COLOURS["background"][0],
            sliderWidth=10, colours=[(255, 255, 255),
                (0, 255, 0), (255, 255, 255)],
            labelShadowOffset=(-1, 1), valueShadowOffset=(-1, 1),
            sliderShadowOffset=(-2, 2), sliderbarShadowOffset=(-2, 2))
        
        self.sliderbars["blue"] = Sliderbar(
            {"multX": 1, "multY": 1}, sliderbarX, sliderStartY+30*2+sliderSpacing*2,
            200, 30, font=SettingsScreen.FONT, minValue=0, maxValue=255,
            label="blue", sliderHeight=30, startValue=SettingsScreen.COLOURS["background"][0],
            sliderWidth=10, colours=[(255, 255, 255),
                (0, 0, 255), (255, 255, 255)],
            labelShadowOffset=(-1, 1), valueShadowOffset=(-1, 1),
            sliderShadowOffset=(-2, 2), sliderbarShadowOffset=(-2, 2))
        
        self.exit_settings = False
        self.save_settings = False
        self.Update(1)

    def UpdateColours(self):
        self.window_surf = self.CreateAASurf(SettingsScreen.SCREENW*0.9,
                                           SettingsScreen.SCREENH*0.9)

    def ChangeColour(self, col):
        self.current_colour = col
        self.sliderbars["red"].value = SettingsScreen.COLOURS[col][0]
        self.sliderbars["red"].calculateSliderPos()
        self.sliderbars["green"].value = SettingsScreen.COLOURS[col][1]
        self.sliderbars["green"].calculateSliderPos()
        self.sliderbars["blue"].value = SettingsScreen.COLOURS[col][2]
        self.sliderbars["blue"].calculateSliderPos()
        for key, value in SettingsScreen.COLOURS.items():
            self.changed_colours[key] = value

    def SaveColours(self):
        for key, value in self.changed_colours.items():
            SettingsScreen.COLOURS[key] = value
        self.save_settings = True
        self.UpdateColours()

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
        r,g,b = self.sliderbars["red"].getValue(), self.sliderbars["green"].getValue(), self.sliderbars["blue"].getValue()
        self.changed_colours[self.current_colour] = (r, g, b)

        for key, btn in self.buttons.items():
            if key.lower() == self.current_colour.lower():
                btn.colours["col1"] = (0, 150, 0)
            else:
                btn.colours["col1"] = SettingsScreen.COLOURS["accent"]
                
        for bar in self.sliderbars.values():
            if sum(SettingsScreen.COLOURS["card-background"])/3 > 200:
                bar.colours[-1] = (0, 0, 0)
            else:
                bar.colours[-1] = (255, 255, 255)

    # Subroutine to render the screen
    def Render(self, screen):
        screen.blit(self.darken_surf, (0, 0))
        screen.blit(self.window_surf, self.window_surf_position)
        self.RenderWidgets(screen)
        pygame.draw.rect(screen, self.changed_colours[self.current_colour], self.colour_preview_rect, 0, 15)
        pygame.draw.rect(screen, (0, 0, 0), self.colour_preview_rect.inflate(5, 5), 5, 15)
        pygame.draw.rect(screen, (255, 255, 255), self.colour_preview_rect.inflate(15, 15), 5, 15)