from abc import ABC, abstractmethod
from itertools import product

class ChessPiece(ABC):
    def __init__(self, name, value, position, color):
        self.name = name
        self.value = value
        self.position = position
        self.color = color


class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__('Pawn', 1, None, color)
        self.color = color
        self.position = position
        self.enpassant_left = False
        self.enpassant_right = False
    
    def get_available_moveset(self, chessgrid):
        available_moveset = set()
        direction = 1 if self.color == 'White' else -1  
        start_row = 2 if self.color == 'White' else 7  

        one_step = (self.position[0], self.position[1] + direction)
        two_step = (self.position[0], self.position[1] + 2 * direction)
        take_piece_left = one_step[0] - 1, one_step[1]
        take_piece_right = one_step[0] + 1, one_step[1]

        if chessgrid[one_step].piece is None:
            available_moveset.add(one_step)
            if self.position[1] == start_row and chessgrid[two_step].piece is None:
                available_moveset.add(two_step)
        
        if one_step[0] - 1 >= 1:
            if chessgrid[take_piece_left].piece is not None and chessgrid[take_piece_left].piece.color != self.color:
                available_moveset.add(take_piece_left)

        if one_step[0] + 1 <= 8:
            if chessgrid[take_piece_right].piece is not None and chessgrid[take_piece_right].piece.color != self.color:
                available_moveset.add(take_piece_right)

        if self.enpassant_left is True:
            available_moveset.add(take_piece_left)

        elif self.enpassant_right is True:
            available_moveset.add(take_piece_right)
        
        return available_moveset


class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__('Bishop', 1, None, color)
        self.color = color
        self.position = position

    def get_available_moveset(self, chessgrid, include=False):
        available_moveset = set()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

        for dx, dy in directions:
            x, y = self.position
           
            while True:
                x += dx
                y += dy

                if not (1 <= x <= 8 and 1 <= y <= 8): 
                    break

                if chessgrid[x,y].piece is None or (isinstance(chessgrid[x,y].piece, King) and chessgrid[x,y].piece.color != self.color):
                    available_moveset.add((x, y))

                else:
                    if chessgrid[x,y].piece.color != self.color: 
                        available_moveset.add((x, y))
                    else:
                        if include is True:
                            available_moveset.add((x, y))
                    break  

        return available_moveset


class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__('Knight', 1, None, color)
        self.color = color
        self.position = position

    def get_available_moveset(self, chessgrid, include=False):
        available_moveset = set()
        porsitions = list(product([2, -2], [1, -1])) + list(product([1, -1], [2, -2]))
        new_porsitions = []

        for x, y in porsitions:
            new_porsitions.append((self.position[0] + x, self.position[1] + y))

        for position in new_porsitions:
            if 1 <= position[0] <= 8 and 1 <= position[1] <= 8:
                if chessgrid[position].piece is None:
                    available_moveset.add(position)
                elif chessgrid[position].piece.color != self.color:
                    available_moveset.add(position)

        return available_moveset
    

class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__('Rook', 1, None, color)
        self.color = color
        self.position = position
        self.castle = True

    def get_available_moveset(self, chessgrid, include=False):
        available_moveset = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dx, dy in directions:
            x, y = self.position

            while True:
                x += dx
                y += dy

                if not (1 <= x <= 8 and 1 <= y <= 8):  
                    break

                if chessgrid[x,y].piece is None or (isinstance(chessgrid[x,y].piece, King) and chessgrid[x,y].piece.color != self.color):
                    available_moveset.add((x, y))

                else:
                    if chessgrid[x,y].piece.color != self.color:  
                        available_moveset.add((x, y))
                    else:
                        if include is True:
                            available_moveset.add((x, y))
                    break  

        return available_moveset

    
class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__('Queen', 1, None, color)
        self.color = color
        self.position = position
    
    def get_available_moveset(self, chessgrid, include= False):
        available_moveset = set()
        rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dx, dy in rook_directions:
            x, y = self.position

            while True:
                x += dx
                y += dy

                if not (1 <= x <= 8 and 1 <= y <= 8):  
                    break

                if chessgrid[x,y].piece is None or (isinstance(chessgrid[x,y].piece, King) and chessgrid[x,y].piece.color != self.color):
                    available_moveset.add((x, y))

                else:
                    if chessgrid[x,y].piece.color != self.color:  
                        available_moveset.add((x, y))
                    else:
                        if include is True:
                            available_moveset.add((x, y))
                    break  
            
            bis_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

            for dx, dy in bis_directions:
                x, y = self.position
            
                while True:
                    x += dx
                    y += dy

                    if not (1 <= x <= 8 and 1 <= y <= 8): 
                        break

                    if chessgrid[x,y].piece is None or (isinstance(chessgrid[x,y].piece, King) and chessgrid[x,y].piece.color != self.color):
                        available_moveset.add((x, y))

                    else:
                        if chessgrid[x,y].piece.color != self.color: 
                            available_moveset.add((x, y))
                        else:
                            if include is True:
                                available_moveset.add((x, y))
                        break  

        return available_moveset


class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__('King', 1, None, color)
        self.color = color
        self.position = position
        self.castle = True

    def get_available_moveset(self, chessgrid, include=False):
        available_moveset = set()
        positions = {(0,1), (0, -1), (1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1)}
        
        if (self.color == 'White' and self.position == (5,1) and self.castle is True):
            if isinstance(chessgrid[(1,1)].piece, Rook):
                if chessgrid[(1,1)].piece.castle is True:
                    if chessgrid[(2,1)].piece is None and chessgrid[(3,1)].piece is None and chessgrid[(4,1)].piece is None:
                        if chessgrid[(2,1)].black_taken is False and chessgrid[(3,1)].black_taken is False and chessgrid[(4,1)].black_taken is False:
                            available_moveset.add((3,1))
            if isinstance(chessgrid[(8,1)].piece, Rook):
                if chessgrid[(8,1)].piece.castle is True:
                    if chessgrid[(6,1)].piece is None and chessgrid[(7,1)].piece is None:
                        if chessgrid[(6,1)].black_taken is False and chessgrid[(7,1)].black_taken is False:
                            available_moveset.add((7,1))

        if (self.color == 'Black' and self.position == (5,8) and self.castle is True):
            if isinstance(chessgrid[(1,8)].piece, Rook):
                if chessgrid[(1,8)].piece.castle is True:
                    if chessgrid[(2,8)].piece is None and chessgrid[(3,8)].piece is None and chessgrid[(4,8)].piece is None:
                        if chessgrid[(2,8)].white_taken is False and chessgrid[(3,8)].white_taken is False and chessgrid[(4,8)].white_taken is False:
                            available_moveset.add((3,8))
            if isinstance(chessgrid[(8,8)].piece, Rook):
                if chessgrid[(8,8)].piece.castle is True:
                    if chessgrid[(6,8)].piece is None and chessgrid[(7,8)].piece is None:
                        if chessgrid[(6,8)].white_taken is False and chessgrid[(7,8)].white_taken is False:
                            available_moveset.add((7,8))

        for dx, dy in positions:
            new_x, new_y = self.position[0] + dx, self.position[1] + dy
            if (1 <= new_x <= 8 and 1 <= new_y <= 8):  
                if 1 <= new_x <= 8 and 1 <= new_y <= 8:
                    taken_square = chessgrid[new_x,new_y].black_taken if self.color == 'White' else chessgrid[new_x,new_y].white_taken
                    if taken_square is False:
                        if chessgrid[new_x, new_y].piece is None:
                            available_moveset.add((new_x, new_y))
                        elif chessgrid[new_x, new_y].piece.color != self.color:
                            available_moveset.add((new_x, new_y))
                    if include is True:
                        available_moveset.add((new_x, new_y))

        
        return available_moveset
    

                

