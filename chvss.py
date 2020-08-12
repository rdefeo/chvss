#!/usr/bin/env python3

import copy
import random

NONE = -1
BLACK = 0
WHITE = 1

EMPTY = '.'
PAWN = 'P'
KNIGHT = 'N'
BISHOP = 'B'
ROOK = 'R'
QUEEN = 'Q'
KING = 'K'

HOME_RANK = [ ROOK, KNIGHT, BISHOP, QUEEN, KING ]
WEIGHTS = { EMPTY:0, PAWN:1, BISHOP:3, KNIGHT:3, ROOK:5, QUEEN:8, KING:20 }
COLOR = { NONE:"*none*", BLACK:"BLACK", WHITE:"WHITE" }

# colors
colW = '\033[93m'      # orange
colB = '\033[96m'      # blue
colE = '\033[35m'      # dark purplish?
colERR = '\033[91m'    # red-ish
colINFO = '\033[94m'   # purple
colCLEAR = '\033[39m'  # reset terminal colors

# Helper methods
def error(msg):
    print(colERR + msg + colCLEAR)
    return False

def info(msg):
    print(colINFO + msg + colCLEAR)
    return True

def opp_color(color):
    if color == WHITE: return BLACK
    if color == BLACK: return WHITE
    if color == NONE: return NONE
    return NONE

def outside_board(r,f):
    if not r in range(0,5): return True
    if not f in range(0,5): return True
    return False

def create_rank(color,piece):
    new_rank = []
    for f in range(5):
        new_rank.append(Piece(color,piece))
    return new_rank

class Piece:
    def __init__(self,color=NONE,piece=EMPTY):
        self.color = color
        self.piece = piece

    def __str__(self):
        col = colE
        if self.color == WHITE: col = colW
        if self.color == BLACK: col = colB
        return col + self.piece + ' '

class Move:
    def __init__(self,p0,r0,f0,p1,r1,f1):
        self.p0 = p0
        self.r0 = r0
        self.f0 = f0
        self.p1 = p1
        self.r1 = r1
        self.f1 = f1
        
    def __str__(self):
        return "{} {},{} to {} {},{}".format(self.p0,self.r0,self.f0,self.p1,self.r1,self.f1)

    def __repr__(self):
        return self.__str__()
    
    # TODO: improve score algo
    def score(self):
        bonus = 2 if WEIGHTS[self.p1] >= WEIGHTS[self.p0] else 0
        return WEIGHTS[self.p1] + bonus
    
class Board:
    def __init__(self):
        pass
    
    def reset(self):
        self.board = [ ]  # 5x5
    
        black_rank = [ ]
        white_rank = [ ]
        bp = HOME_RANK[:] # force a copy by slicing
        wp = HOME_RANK[:]
        # randomize the home ranks
        random.shuffle(bp)
        random.shuffle(wp)
        for f in range(5):
            white_rank.append(Piece(WHITE,wp[f]))
            black_rank.append(Piece(BLACK,bp[f]))
        self.board.append(white_rank)
        self.board.append(create_rank(WHITE,PAWN))
        self.board.append(create_rank(NONE,EMPTY))
        self.board.append(create_rank(BLACK,PAWN))
        self.board.append(black_rank)
    
    def display(self):
        for r in range(5):
            print(colCLEAR + str(5-r) + ' ',end='') # rank
            for f in range(5):
                print(self.board[4-r][f],end='')
            print('')
        print(colCLEAR + "  a b c d e") # file

    def create_move(self,mstr):
        m = mstr.lower().split()
        if len(m) < 2 or len(m[0]) != 2 or len(m[1]) != 2:
            return error("Invalid move: " + mstr)
        if (not m[0][0] in "abcde") or (not m[0][1] in "12345"):
            return error("Invalid beginning position: " + m[0])
        if (not m[1][0] in "abcde") or (not m[1][1] in "12345"):
            return error("Invalid ending position: " + m[1])
        if m[0] == m[1]:
            return error("Starting and ending positions are the same")

        # convert to file and rank coordinates
        f0 = ord(m[0][0])-ord('a')
        r0 = int(m[0][1])-1

        f1 = ord(m[1][0])-ord('a')
        r1 = int(m[1][1])-1

        # did they select their own piece?
        if self.board[r0][f0].color != WHITE:
            return error("Must select your own piece to move")

        # trying to move to square occupied by self?
        if self.board[r1][f1].color == WHITE:
            return error("Destination square occupied")

        return Move(self.board[r0][f1].piece,r0,f0,self.board[r1][f1].piece,r1,f1)
        
    def square_attacked_by(self, color, r1, f1):
        # for each piece of 'color', is moving to r1,f1 valid?
        # if so, then it's considered under attack
        for r in range(5):
            for f in range(5):
                if self.board[r][f].color == color:
                    if self.valid_move(color,r,f,r1,f1,True)[0]: # valid_move for attack_only=True
                        return True
        return False
    
    # returns [ T/F, Move ]
    def valid_move(self,color,r0,f0,r1,f1,attack_only=False):
        # sanity checks
        if outside_board(r1,f1): return [False,None]
        if (r0,f0) == (r1,f1): return [False,None]
        if self.board[r0][f0].color == self.board[r1][f1].color: return [False]
        
        piece = self.board[r0][f0].piece.upper();
        method_name = 'valid_move_for_' + piece
        method = getattr(self,method_name,lambda: False)
        valid_move = method(color,r0,f0,r1,f1)
        if valid_move:
            pass
        return [valid_move, Move(piece,r0,f0,self.board[r1][f1].piece,r1,f1)]
        
    def valid_move_for_P(self,color,r0,f0,r1,f1,attack_only=False):
        if color == WHITE and r1-r0 != 1: return False
        if color == BLACK and r0-r1 != 1: return False

        if abs(f1-f0) > 1: return False
        
        if f0 == f1:
            if self.board[r1][f1].color == NONE and not attack_only: return True
        elif self.board[r1][f1].color == opp_color(color):
            return True # pawn capture!

        return False

    def valid_move_for_R(self,color,r0,f0,r1,f1):
        if r0 == r1:
            step = -1 if f0>f1 else 1
            for s in range(f0+step, f1, step):
                if not self.board[r0][s].color == NONE:
                    return False
            return True
        elif f0 == f1:
            step = -1 if r0>r1 else 1            
            for s in range(r0+step, r1, step):
                if not self.board[s][f0].color == NONE:
                    return False
            return True
        return False

    def valid_move_for_B(self,color,r0,f0,r1,f1):
        if abs(r1-r0) != abs(f1-f0): return False
        f = f0
        rstep = -1 if r0>r1 else 1
        fstep = -1 if f0>f1 else 1
        for s in range(r0+rstep, r1, rstep):
            f = f + fstep
            if not self.board[s][f].color == NONE:
                return False
        return True

    def valid_move_for_N(self,color,r0,f0,r1,f1):
        if abs(r1-r0) == 2 and abs(f1-f0) == 1: return True
        if abs(r1-r0) == 1 and abs(f1-f0) == 2: return True        
        return False

    def valid_move_for_K(self,color,r0,f0,r1,f1):
        if abs(r1-r0) > 1 or abs(f1-f0) > 1: return False
        if self.square_attacked_by(opp_color(color),r1,f1) and color == WHITE:
            error("King cannot put himself in check")
            return False
        return True

    def valid_move_for_Q(self,color,r0,f0,r1,f1):
        if self.valid_move_for_R(color,r0,f0,r1,f1) or self.valid_move_for_B(color,r0,f0,r1,f1):
            return True;
        return False

    def try_move_piece(self,move,color):
        # validate that the piece can move to the desired location
        vm = self.valid_move(color,move.r0,move.f0,move.r1,move.f1)
        if not vm[0]:
            return error("Invalid move for piece " + self.board[move.r0][move.f0].piece)
    
        # if it's valid, move the piece on a temp board and check for check/mate
        nb = copy.deepcopy(self)
        nb.board[move.r1][move.f1] = nb.board[move.r0][move.f0]
        nb.board[move.r0][move.f0] = Piece()
            
        if nb.king_in_check(color):
            return False #error("Can not place self in check!")

        return True
    
    # move is a Move obj, color of who is making move
    def move_piece(self,move,color):
        if move.p1 != EMPTY:
            print("Capturing "+move.p1+"!!")
            
        # move the piece and mark current square empty
        self.board[move.r1][move.f1] = self.board[move.r0][move.f0]
        self.board[move.r0][move.f0] = Piece()
        
    # Generate a move for the computer (BLACK)    
    def generate_move(self):
        # for all pieces (BLACK), generate all *valid* moves
        # for each move, compute score for how good
        # 'move' is 'a2 a3'
        moves = []
        for r in range(5):
            for f in range(5):
                if self.board[r][f].color == BLACK:
                    piece = self.board[r][f].piece.upper()
                    method_name = 'generate_moves_for_' + piece
                    method = getattr(self,method_name,lambda x, y: [])
                    moves += method(r,f)
        moves = list(filter(lambda x: True if x[0] == True else False, moves))
#        print(moves)

        if len(moves) == 0:
            error("No valid moves! Checkmate??")
            return None
        
        # sort moves based on score
        moves = sorted(moves,key=lambda m: m[1].score(),reverse=True)
        for m in moves:
            if self.try_move_piece(m[1],BLACK):
#                print("Best move is: ",end='')
#                print(m[1])
                return m[1]
        return None
    
    def generate_moves_for_P(self,r,f):
        moves = []
        moves += [self.valid_move(BLACK,r,f,r-1,f-1)]
        moves += [self.valid_move(BLACK,r,f,r-1,f)]
        moves += [self.valid_move(BLACK,r,f,r-1,f+1)]
        return moves

    def generate_moves_for_R(self,r,f):
        moves = []
        for r1 in range(0,5):  # vert
            moves += [self.valid_move(BLACK,r,f,r1,f)]
        for f1 in range(0,5):  # horiz
            moves += [self.valid_move(BLACK,r,f,r,f1)]
        return moves

    def generate_moves_for_B(self,r,f):
        moves = []
        sr_down = r + f - 1
        sr_up = r - f
        for f1 in range(0,5):
            moves += [self.valid_move(BLACK,r,f,sr_down,f1)]
            moves += [self.valid_move(BLACK,r,f,sr_up,f1)]
            sr_down = sr_down -1
            sr_up = sr_up + 1
        return moves
    
    def generate_moves_for_N(self,r,f):
        moves = []
        moves += [self.valid_move(BLACK,r,f,r+2,f+1)]
        moves += [self.valid_move(BLACK,r,f,r+1,f+2)]
        moves += [self.valid_move(BLACK,r,f,r-1,f+2)]
        moves += [self.valid_move(BLACK,r,f,r-2,f+1)]

        moves += [self.valid_move(BLACK,r,f,r-2,f-1)]
        moves += [self.valid_move(BLACK,r,f,r-1,f-2)]
        moves += [self.valid_move(BLACK,r,f,r+1,f-2)]
        moves += [self.valid_move(BLACK,r,f,r+2,f-1)]

        return moves

    def generate_moves_for_Q(self,r,f):
        moves = []
        moves += self.generate_moves_for_R(r,f)
        moves += self.generate_moves_for_B(r,f)
        return moves

    def generate_moves_for_K(self,r,f):
        moves = []
        moves += [self.valid_move(BLACK,r,f,r+1,f-1)]
        moves += [self.valid_move(BLACK,r,f,r+1,f+0)]
        moves += [self.valid_move(BLACK,r,f,r+1,f+1)]
        moves += [self.valid_move(BLACK,r,f,r+0,f-1)]
        moves += [self.valid_move(BLACK,r,f,r-0,f+1)]
        moves += [self.valid_move(BLACK,r,f,r-1,f-1)]
        moves += [self.valid_move(BLACK,r,f,r-1,f+0)]
        moves += [self.valid_move(BLACK,r,f,r-1,f+1)]
        return moves

    def select_best_move(self,moves):
        moves = sorted(moves,key=lambda x: x[1].score(),reverse=True)
#        print("Sorted: ",end='')
#        print(moves)
        return moves[0][1]

    def king_in_check(self,color):
        # find the 'color' king
        for r in range(5):
            for f in range(5):
                if self.board[r][f].color == color and self.board[r][f].piece == KING:
                    if self.square_attacked_by(opp_color(color),r,f):
                        return True
                    return False

    
board = Board()
board.reset()

while(1):
    board.display()
    # player move
    mstr = input("Move? ")
    if mstr == '' or mstr.lower() == 'q': quit()
    
    # turn user input into Move obj
    move = board.create_move(mstr)
    if isinstance(move, Move) and board.try_move_piece(move,WHITE) == True:
        board.move_piece(move,WHITE)
    else:
        continue # bad move, try again

    # display user's move
    board.display()
    
    # computer select move
    move = board.generate_move()
    if isinstance(move, Move):
#        print("Moving piece: "+str(move))
        board.move_piece(move,BLACK)
    else:
        if board.king_in_check(BLACK):
            info("CHECKMATE!")
            ng = input("New game? (Y/n): ")
            if ng.lower() == 'n': quit()
            board.reset()





