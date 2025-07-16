from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from pieces import *
import re

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)
    def on_focus(self, instance, value):
        Clock.temp = float(instance.text)
    
class Clock(Label):
    a = NumericProperty(0)  
    temp = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temp = self.a

    def start(self, chessgrid_dict):
        Animation.cancel_all(self) 
        self.anim = Animation(a = 0, duration = self.a)
 
        def finish_callback(animation, clock):
            clock.text = "FINISHED"
            for button in chessgrid_dict.values():
                button.disabled = True
 
        self.anim.bind(on_complete = finish_callback)
        self.anim.start(self)
    
    def reset(self):
        Animation.cancel_all(self)
        self.a = self.temp
        self.text = str(self.a)
 
    def on_a(self, instance, value):
        self.text = str(round(value, 1))

class ChessButton(Button):
    DARK = (0.2, 0.6, 0.8, 1)
    LIGHT = (1, 1, 1, 1)

    def __init__(self, piece, position, square, **kwargs):
        super().__init__(**kwargs)
        self.piece = piece
        self.position = position
        self.square = square
        self.white_taken = False
        self.black_taken = False
        with self.canvas.after:
            Color(0, 0, 0, 1)  
            self.border_line = Line(rectangle=self.pos + self.size, width=0.5)

        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border_line.rectangle = self.pos + self.size

    def on_background_normal(self, instance, value):
        self.background_disabled_normal = value

    def update_image(self):
        self.background_color = self.LIGHT if self.square == 'Light' else self.DARK
            
        if self.piece is None:
            self.background_normal = ''
            self.disabled = True

        elif isinstance(self.piece, Pawn):
            if self.piece.color == 'White':
                self.background_normal = 'image/wp.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/bp.png'

        elif isinstance(self.piece, Knight):
            if self.piece.color == 'White':
                self.background_normal = 'image/wn.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/bn.png'

        elif isinstance(self.piece, Bishop):
            if self.piece.color == 'White':
                self.background_normal = 'image/wb.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/bb.png'

        elif isinstance(self.piece, Rook):
            if self.piece.color == 'White':
                self.background_normal = 'image/wr.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/br.png'
        
        elif isinstance(self.piece, Queen):
            if self.piece.color == 'White':
                self.background_normal = 'image/wq.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/bq.png'

        elif isinstance(self.piece, King):
            if self.piece.color == 'White':
                self.background_normal = 'image/wk.png'
            elif self.piece.color == 'Black':
                self.background_normal = 'image/bk.png'
    




            






