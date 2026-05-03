# Import modules
import pygame, random
from scripts.widgets import *
from scripts.screens import *
from scripts.text_box import Textbox

# Create the class for the start screen and inherit from the main screen class
class UserInterface(Screen):
    SCREENW, SCREENH = None, None
    FONT = None
    COLOURS = None
    ASSETS = None
    CARDS = None
    SMALLFONT = None
    # Initialise the class
    def __init__(self):
        # Initialise the parent class
        super().__init__()
        self.text_box = Textbox(UserInterface.SCREENW*0.96, UserInterface.SCREENH*0.5)
        
        self.buttons["settings"] = Button(
            sprite=UserInterface.ASSETS["settings-icon"], drawBackground=False,
            text="", posX=UserInterface.SCREENW*0.005, posY=UserInterface.SCREENH*0.93,
            command=self.ShowSettings)
        
        self.buttons["previous"] = Button(
            posX=UserInterface.SCREENW*0.02, posY=UserInterface.SCREENH*0.55,
            width=120, height=25, font=UserInterface.FONT, text="Previous",
            curve=15, textShadowOffset=(-1, 1), command=self.ChangeQuestion,
            parameters=[-1]
        )
        
        self.buttons["next"] = Button(
            posX=UserInterface.SCREENW*0.74, posY=UserInterface.SCREENH*0.55,
            width=120, height=25, font=UserInterface.FONT, text="Next",
            curve=15, textShadowOffset=(-1, 1), command=self.ChangeQuestion,
            parameters=[1]
        )
        
        self.in_settings = False
        
        SettingsScreen.SCREENW = UserInterface.SCREENW
        SettingsScreen.SCREENH = UserInterface.SCREENH
        SettingsScreen.FONT = UserInterface.FONT
        SettingsScreen.COLOURS = UserInterface.COLOURS
        self.settings_screen = SettingsScreen()
        
        self.question_idx = 0
        self.topics = list(UserInterface.CARDS.keys())
        self.topic = random.choice(self.topics)
        self.total_questions = len(list(UserInterface.CARDS[self.topic].keys()))
        self.question = list(UserInterface.CARDS[self.topic].keys())[self.question_idx]
        self.answer = UserInterface.CARDS[self.topic][self.question]
        
        self.mouseRect = pygame.Rect(0, 0, 1, 1)
        self.topicChoiceList = Droplist({"multX":1, "multY":1},
            currentItem="ads", font=UserInterface.SMALLFONT, textFont=UserInterface.FONT,
            x=UserInterface.SCREENW*0.02, y=UserInterface.SCREENH*0.7,
            width=100, height=25, items=self.topics, label="Topic",
            textShadowOffset=(-1, 1), labelShadowOffset=(-1, 1),
            scrollbarWidth=5, labelSpacing=13, curve=15)

    def ChangeQuestion(self, dir):
        self.question_idx += dir
        self.text_box.card_side = "question"
        if self.question_idx >= self.total_questions:
            self.question_idx = self.total_questions-1
        elif self.question_idx <= 0:
            self.question_idx = 0
            
    # Subroutine to show the settings
    def ShowSettings(self):
        self.in_settings = True
        
    # Subroutine to update the screen
    def Update(self, delta_time):
        self.mouseRect.topleft = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.colours["col1"] = UserInterface.COLOURS["accent"]
        self.topicChoiceList.colours[0] = UserInterface.COLOURS["accent"]
        if not self.in_settings:
            self.UpdateWidgets(delta_time)
            self.text_box.Update()
            self.topicChoiceList.update(self.mouseRect)
        else:
            self.settings_screen.Update(delta_time)
        
        if self.settings_screen.exit_settings == True and self.in_settings:
            self.in_settings = False
            self.settings_screen.exit_settings = False
            
        self.text_box.answer_txt = self.answer
        self.text_box.question_txt = self.question
        
        self.topic = self.topicChoiceList.currentItem
        self.total_questions = len(list(UserInterface.CARDS[self.topic].keys()))
        self.question = list(UserInterface.CARDS[self.topic].keys())[self.question_idx]
        self.answer = UserInterface.CARDS[self.topic][self.question]
        
    # Subroutine to render the screen
    def Render(self, screen):
        self.text_box.Draw(screen)
        self.RenderWidgets(screen)
        
        self.topicChoiceList.draw(screen)
        
        if self.in_settings:
            self.settings_screen.Render(screen)