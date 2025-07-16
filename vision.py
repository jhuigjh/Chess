from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from imports import *
import random
from chessboard import Chessboard

class ChessVision(Screen, Chessboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Scoreboard and Settings
        input = FloatInput(hint_text = "Enter duration (seconds)", size_hint = (0.15, 1))
        input.text = ("15")

        reset_button = Button(text=f"Reset",  background_color=(0.2, 0.6, 0.8, 1), size_hint = (0.15, 1))
        start_button = Button(text=f"Start",  background_color=(0.2, 0.6, 0.8, 1), size_hint = (0.15, 1))
        start_button.bind(on_press=lambda instance: self.start(instance))
        reset_button.bind(on_press=lambda instance: self.reset(start_button))

        self.score = 0
        self.clock = Clock(size_hint = (0.2,1), a = float(input.text))
        self.scoreboard = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding = 5)
        self.label = Label(text='[color=93fff0]' + "Notation" + '[/color]', size_hint=(0.05, 1), markup = True)
        self.score_label = Label(text='[color=93fff0]' + str(self.score) + '[/color]', size_hint=(0.05, 1), markup = True)
        
        self.scoreboard.add_widget(self.label)
        self.scoreboard.add_widget(self.clock)
        self.scoreboard.add_widget(input)
        self.scoreboard.add_widget(reset_button)
        self.scoreboard.add_widget(start_button)
        self.scoreboard.add_widget(self.score_label)
        self.main_layout.add_widget(self.scoreboard)
     
        self.main_layout.add_widget(self.layout)

        self.add_widget(self.main_layout)
        
        
    def reset(self, instance):
        self.clock.reset()
        instance.disabled = False 
        self.label.text = '[color=93fff0]' + "Notation" + '[/color]'
        self.disable_chessgrid()
        self.score = 0
        self.score_label.text = f"{self.score}"

    def start(self, instance):
        if not instance.disabled:  
            self.clock.start(self.chessgrid)
            instance.disabled = True  
            self.get_random_key()
            self.enable_chessgrid()

    def get_random_key(self):
        key_list = []
        for key in self.chessgrid.values():
            key_list.append(key.text)
        random_key = random.choice(key_list)
        self.label.text = '[color=93fff0]' + "" + f'{random_key}' +'[/color]'
        self.key = random_key
    
    def play_chessvision(self, instance):
        if instance.text == self.key:
            self.score += 1
            self.score_label.text = f"{self.score}"
            self.get_random_key()





