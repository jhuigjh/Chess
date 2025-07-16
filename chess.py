from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from chessboard import Chessboard
from pieces import *

class ChessGame(Screen, Chessboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.turn = 'White'
        self.available_moveset = set()
        self.enpassant_pawn = None
        self.left_pawn = None
        self.right_pawn = None
        self.white_king = None
        self.black_king = None
        self.promote_layout = BoxLayout(orientation='vertical', padding = 0)
        self.color_generator = self.yield_color()
        self.add_widget(self.layout)
        self.game()

        Window.clearcolor = (0.17, 0.17, 0.17, 1)

    def show_promotion_options(self, piece):
        if self.promote_layout.parent:
            self.promote_layout.parent.remove_widget(self.promote_layout)  

        self.promote_layout.clear_widgets()  

        white = ['image/wq.png', 'image/wr.png', 'image/wb.png', 'image/wn.png']
        black = ['image/bq.png', 'image/br.png', 'image/bb.png', 'image/bn.png']

        images = white if self.turn == 'White' else black
        for image in images:
            button = Button(background_normal=image, size_hint=(0.2, 0.1), pos_hint={"right": 1})
            self.promote_layout.add_widget(button)
            button.bind(on_press=lambda instance, p=piece: self.callback_promote(instance, p))

        self.add_widget(self.promote_layout)  


    def callback_promote(self, instance, promoted_piece):
        piece_color = 'White' if promoted_piece.color == 'White' else 'Black'
        if "image/wq.png" == instance.background_normal or "image/bq.png" == instance.background_normal:
            self.chessgrid[promoted_piece.position].piece = Queen(color=piece_color, position = promoted_piece.position)
        elif "image/wr.png" == instance.background_normal or "image/br.png" == instance.background_normal:
            self.chessgrid[promoted_piece.position].piece = Rook(color=piece_color, position = promoted_piece.position)
        elif "image/wb.png" == instance.background_normal or "image/bb.png" == instance.background_normal:
            self.chessgrid[promoted_piece.position].piece = Bishop(color=piece_color, position = promoted_piece.position)
        else:
            self.chessgrid[promoted_piece.position].piece = Knight(color=piece_color, position = promoted_piece.position)
        self.chessgrid[promoted_piece.position].update_image()
        self.update_taken(self.chessgrid[promoted_piece.position])
        self.promote_layout.clear_widgets()  
        self.change_turn(self.turn)

        # Show king in check
        if self.turn == 'Black':
            if self.chessgrid[self.black_king.position].white_taken is True:
                self.chessgrid[self.black_king.position].background_color = (1,0.5,0.5,1)
        elif self.turn == 'White':
            if self.chessgrid[self.white_king.position].black_taken is True:
                self.chessgrid[self.white_king.position].background_color = (1,0.5,0.5,1)

    def game(self):
        self.starting_position()

    def starting_position(self):
        for button in self.chessgrid.values():
            button.background_normal = ''
            button.disabled = False
            if button.position[1] == 2:
                button.piece = Pawn(color='White', position = button.position)
            elif button.position[1] == 7:
                button.piece = Pawn(color='Black', position = button.position)
            elif button.position[1] == 1:  # White's back rank
                if button.position[0] in [1, 8]:
                    button.piece = Rook(color='White', position = button.position)
                elif button.position[0] in [2, 7]:
                    button.piece = Knight(color='White', position = button.position)
                elif button.position[0] in [3, 6]:
                    button.piece = Bishop(color='White', position = button.position)
                elif button.position[0] == 4:
                    button.piece = Queen(color='White', position = button.position)
                elif button.position[0] == 5:
                    button.piece = King(color='White', position = button.position)
                    self.white_king = button.piece

            elif button.position[1] == 8:  # Black's back rank
                if button.position[0] in [1, 8]:
                    button.piece = Rook(color='Black', position = button.position)
                elif button.position[0] in [2, 7]:
                    button.piece = Knight(color='Black', position = button.position)
                elif button.position[0] in [3, 6]:
                    button.piece = Bishop(color='Black', position = button.position)
                elif button.position[0] == 4:
                    button.piece = Queen(color='Black', position = button.position)
                elif button.position[0] == 5:
                    button.piece = King(color='Black', position = button.position)
                    self.black_king = button.piece
            else:
                button.disabled = True
            button.update_image()

        for button in self.chessgrid.values():
            self.update_taken(button)

        self.white_turn()

    def shrink_available_moveset(self):
        king_instance = False
        if isinstance(self.instance.piece, King):
            king_instance = True
        new_available_moveset = set()
        original_grid = {pos: (square.piece, square.black_taken, square.white_taken) for pos, square in self.chessgrid.items()}  # Manual copy
        for position in self.available_moveset:

            # Enpassant special case
            if self.enpassant_pawn is not None:
                direction = 1 if self.instance.piece.color == 'White' else -1
                if position == (self.enpassant_pawn.position[0], self.enpassant_pawn.position[1] + direction):
                    if self.instance.piece != self.enpassant_pawn:
                        self.chessgrid[self.enpassant_pawn.position].piece = None 
            
            self.chessgrid[position].piece = self.instance.piece
            self.chessgrid[self.instance.piece.position].piece = None 
            
            self.reset_taken()
            for button in self.chessgrid.values():
                self.update_taken(button)
            if self.turn == 'White':
                if king_instance:
                    if self.chessgrid[position].black_taken is False:
                        new_available_moveset.add(position)
                elif self.chessgrid[self.white_king.position].black_taken is False:
                    new_available_moveset.add(position)
            elif self.turn == 'Black':
                if king_instance:
                    if self.chessgrid[position].white_taken is False:
                        new_available_moveset.add(position)                
                elif self.chessgrid[self.black_king.position].white_taken is False:
                    new_available_moveset.add(position)
            for pos, (piece, black_taken, white_taken) in original_grid.items():
                self.chessgrid[pos].piece = piece
                self.chessgrid[pos].black_taken = black_taken
                self.chessgrid[pos].white_taken = white_taken
            self.available_moveset = new_available_moveset
    
    def choose_piece(self, instance):
        self.instance = instance
        self.available_moveset = instance.piece.get_available_moveset(self.chessgrid)
        self.shrink_available_moveset()

    def move_piece(self, instance):
        if instance.position in self.available_moveset:
            # Enable enpassant for adjacent pawns
            if isinstance(self.instance.piece, Pawn):
                if self.left_pawn is not None:
                    self.left_pawn.enpassant_left = None
                if self.right_pawn is not None:
                    self.right_pawn.enpassant_right = None

                if instance.position[0] == self.instance.position[0] and abs(instance.position[1] - self.instance.position[1]) == 2:
                    self.left_pawn, self.right_pawn = self.enable_enpassant(instance)
                else: 
                    self.take_enpassant(instance)
            
            # Promotion
            promoting = False
            if isinstance(self.instance.piece, Pawn):
                row = instance.position[1]  
                if (self.turn == 'White' and row == 8) or (self.turn == 'Black' and row == 1):
                    self.show_promotion_options(self.instance.piece) 
                    promoting = True

            # Castling
            if isinstance(self.instance.piece, King):
                self.king_castle(instance)
                self.instance.piece.castle = False
            if isinstance(self.instance.piece, Rook):
                self.instance.piece.castle = False
  
            # Update the current button
            instance.piece = self.instance.piece
            instance.piece.position = instance.position
            # Update the last button
            self.instance.piece = None

            return promoting
    
    def enable_enpassant(self, instance):
        left_pawn = None
        right_pawn = None
        if instance.position[0] - 1 >= 1:
            if isinstance(self.chessgrid[(instance.position[0] - 1, instance.position[1])].piece, Pawn):
                if self.instance.piece.color != self.chessgrid[(instance.position[0] - 1, instance.position[1])].piece.color:
                    self.chessgrid[(instance.position[0] - 1, instance.position[1])].piece.enpassant_right = True   
                    self.enpassant_pawn = self.instance.piece
                    right_pawn = self.chessgrid[(instance.position[0] - 1, instance.position[1])].piece
                
        if instance.position[0] + 1 <= 8:
            if isinstance(self.chessgrid[(instance.position[0] + 1, instance.position[1])].piece, Pawn):
                if self.instance.piece.color != self.chessgrid[(instance.position[0] + 1, instance.position[1])].piece.color:
                    self.chessgrid[(instance.position[0] + 1, instance.position[1])].piece.enpassant_left = True
                    self.enpassant_pawn = self.instance.piece
                    left_pawn = self.chessgrid[(instance.position[0] + 1, instance.position[1])].piece
        return (left_pawn, right_pawn)
        
    def take_enpassant(self, instance):
        if self.enpassant_pawn is not None:
            direction = 1 if self.instance.piece.color == 'White' else -1
            if instance.position == (self.enpassant_pawn.position[0], self.enpassant_pawn.position[1] + direction):
                if self.instance.piece != self.enpassant_pawn:
                    self.chessgrid[self.enpassant_pawn.position].piece = None  
        
        self.enpassant_pawn = None
        self.instance.piece.enpassant_left = False
        self.instance.piece.enpassant_right = False

    def king_castle(self, instance):
        if self.instance.piece.castle is True:
            if self.instance.piece.color == 'White':
                if instance.position == (3,1):
                    if self.chessgrid[1,1].piece.castle is True:
                        self.chessgrid[4,1].piece = self.chessgrid[1,1].piece
                        self.chessgrid[4,1].piece.position = (4,1)
                        self.chessgrid[1,1].piece = None
                elif instance.position == (7,1):
                    if self.chessgrid[8,1].piece.castle is True:
                        self.chessgrid[6,1].piece = self.chessgrid[8,1].piece
                        self.chessgrid[6,1].piece.position = (6,1)
                        self.chessgrid[8,1].piece = None
            if self.instance.piece.color == 'Black':
                if instance.position == (3,8):
                    if self.chessgrid[1,8].piece.castle is True:
                        self.chessgrid[4,8].piece = self.chessgrid[1,8].piece
                        self.chessgrid[4,8].piece.position = (4,8)
                        self.chessgrid[1,8].piece = None
                elif instance.position == (7,8):
                    if self.chessgrid[8,8].piece.castle is True:
                        self.chessgrid[6,8].piece = self.chessgrid[8,8].piece
                        self.chessgrid[6,8].piece.position = (6,8)
                        self.chessgrid[8,8].piece = None
        
    def white_turn(self):
        for button in self.chessgrid.values():
            if button.piece is None:
                pass
            else:
                button.disabled = False if button.piece.color == "White" else True

    def black_turn(self):
        for button in self.chessgrid.values():
            if button.piece is None:
                pass
            else:
                button.disabled = False if button.piece.color == "Black" else True
 
    def change_turn(self, color):
        self.white_turn() if color == "White" else self.black_turn()

    def yield_color(self):
        while True:
            yield 'Black'
            yield 'White'

    def reset_taken(self):
        for button in self.chessgrid.values():
            button.white_taken = False
            button.black_taken = False

    def update_taken(self, button):
        if button.piece is None:
            return

        if isinstance(button.piece, Pawn):
            taken_squares = set()
            direction = 1 if button.piece.color == 'White' else -1  
            x, y = button.piece.position

            if 1 <= x - 1 <= 8 and 1 <= y + direction <= 8:
                taken_squares.add((x - 1, y + direction))
            if 1 <= x + 1 <= 8 and 1 <= y + direction <= 8:
                taken_squares.add((x + 1, y + direction))

            for square in taken_squares:
                if button.piece.color == 'White':
                    self.chessgrid[square].white_taken = True
                else:
                    self.chessgrid[square].black_taken = True
                    
        else:  
            taken_squares = button.piece.get_available_moveset(self.chessgrid, include=True)
            for square in taken_squares:
                if button.piece.color == 'White':
                    self.chessgrid[square].white_taken = True
                else:
                    self.chessgrid[square].black_taken = True

    

    