from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from imports import *


class Chessboard:
    def __init__(self):
        
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.labels = [] # Uodate label in list
        # Top labels
        self.top_labels = FloatLayout(size_hint=(1, 0.1), pos_hint={"center_x": 0.56, "center_y": 0.5})
        for index, col in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
            label = Label(text=col, size_hint=(0.1, 1), pos_hint={"x": index * 0.088, "center_y": 0.5})
            self.top_labels.add_widget(label)
            self.labels.append(label)

        # Grid with side labels
        self.side_labels_and_grid = BoxLayout(orientation='horizontal')

        # Add side row labels
        self.side_labels = BoxLayout(orientation='vertical', size_hint=(0.005, 1))
        self.side_padding = BoxLayout(orientation='vertical', size_hint=(0.01, 1))
        for row in range(8, 0, -1):
            label = Label(text=str(row))
            self.side_labels.add_widget(label)
            self.labels.append(label)
        self.side_labels_and_grid.add_widget(self.side_labels)

        # Add chessboard grid
        self.chessgrid = {}
        self.grid_layout = GridLayout(cols=8, rows=8, size_hint = (0.035, 1))

        for row in range(8, 0, -1):
            for col_index, col in enumerate('abcdefgh', start=1):
                square_color = "Dark" if (row + col_index) % 2 == 0 else "Light"
                background = (0.2, 0.6, 0.8, 1) if square_color == "Dark" else (1, 1, 1, 1)

                button = ChessButton(
                    text=f'{col}{row}',
                    square=square_color,
                    font_size=0,
                    background_normal='',
                    background_color=background,
                    disabled=True,
                    piece=None,
                    position=(col_index, row)
                )

                button.bind(on_press=self.callback)
                self.chessgrid[button.position] = button
                self.grid_layout.add_widget(button)

        self.side_labels_and_grid.add_widget(self.grid_layout)
        self.side_labels_and_grid.add_widget(self.side_padding)
    
        self.layout.add_widget(self.top_labels)
        self.layout.add_widget(self.side_labels_and_grid)

    def callback(self, instance):
        def highlight_square(square):
            return (1, 1, 0.5, 1) if square == "Dark" else (1, 1, 0.75, 1)
            
        if self.name == "chessvision":
            if instance.text == self.key:
                self.score += 1
                self.score_label.text = f"{self.score}"
                self.get_random_key()

        if self.name == "chessgame":
            for button in self.chessgrid.values():
                button.update_image()
            
            for item in self.available_moveset:
                self.chessgrid[item].disabled = True

            if isinstance(instance.piece, ChessPiece) and instance.piece.color == self.turn:
                self.choose_piece(instance)
                for item in self.available_moveset:
                    self.chessgrid[item].disabled = False
                    self.chessgrid[item].background_color = (0.5,1,0.83,1)
                self.chessgrid[instance.position].background_color = (0.5,0.87,0.66,1)
            else:
                promoting_bool = self.move_piece(instance)
                self.reset_taken()

                for button in self.chessgrid.values():
                    button.update_image()
                    self.update_taken(button)

                # Show last move
                self.instance.background_color = highlight_square(self.instance.square)
                self.chessgrid[instance.position].background_color = highlight_square(self.chessgrid[instance.position].square)

                # Next turn
                color = next(self.color_generator)
                self.change_turn(color)
                self.turn = color

                if promoting_bool:
                    self.disable_chessgrid()
            
                # Show king in check
                if self.turn == 'Black':
                    if self.chessgrid[self.black_king.position].white_taken is True:
                        self.chessgrid[self.black_king.position].background_color = (1,0.5,0.5,1)
                elif self.turn == 'White':
                    if self.chessgrid[self.white_king.position].black_taken is True:
                        self.chessgrid[self.white_king.position].background_color = (1,0.5,0.5,1)

                # Check for checkmates
                checkmate = True
                for button in self.chessgrid.values():
                    if button.piece is not None:
                        if button.piece.color == self.turn:
                            self.choose_piece(button)      
                            if self.available_moveset:
                                checkmate = False
                if checkmate:
                    print('Checkmate')
           

                

                
    def enable_chessgrid(self):
        for button in self.chessgrid.values():
            button.disabled = False

    def disable_chessgrid(self):
        for button in self.chessgrid.values():
            button.disabled = True
    

 
