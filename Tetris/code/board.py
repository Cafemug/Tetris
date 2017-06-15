from global_var import *
from user_interface import *
import pygame
class Board(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(caption)
        pygame.key.set_repeat(300, 40)
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.width = (cols+side_space)*blockSize
        self.height = rows*blockSize
        self.bg = []
        self.board = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.init_new_game()

    def init_new_game(self):
        self.next_piece = pieces[rand(len(pieces))]
        self.piece_x = (cols/2)
        self.piece_y = 0
        self.new_piece()
        self.userevent_firetime = 1000
        self.new_row_firetime = 30000
        pygame.time.set_timer(pygame.USEREVENT+1, self.userevent_firetime)
        pygame.time.set_timer(pygame.USEREVENT+2, self.new_row_firetime)
        self.init_board()
        self.init_bg()
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.gameExit = False
        self.pause = False
        self.score = 0
        self.level = 1

    def init_bg(self):
        del self.bg
        self.bg = []
        for i in range(rows):
            ls = []
            for j in range(cols):
                ls.append(0 if i%2==j%2 else 1)
            self.bg.append(ls)

    def init_board(self):
        del self.board
        self.board = []
        for i in range(rows):
            ls = []
            for j in range(cols):
                ls.append(0)
            self.board.append(ls)
        ls = []
        for i in range(cols):
            ls.append(1)
        self.board.append(ls)

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = pieces[rand(len(pieces))]
        self.piece_x = int((cols-len(self.piece[0]))/2)
        self.piece_y = 0
        if not self.check_ok(self.piece, (self.piece_x, self.piece_y)):
            self.gameOver = True


    def make_done(self, piece, off=(0,0)):
        if self.pause or self.gameOver:
            return
        pygame.mixer.Sound.play(self.done_sound)
        #pygame.image.load("bangblue.png")

        off_x = off[0]
        off_y = off[1]-1
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x]:
                    self.board[y+off_y][x+off_x] = piece[y][x]
        self.score += 10

    def delete_row(self, i):
        if self.pause or self.gameOver:
            return

        del self.board[i]

        self.board = [[0 for i in range(cols)]] + self.board

    def push_new_row(self):
        if self.pause or self.gameOver:
           return
        del self.board[0]
        ls = []
        for i in range(cols):
            random_bool = rand(2)
            if random_bool:
                ls.append(rand(len(colors)-2)+2)
            else:
                ls.append(0)
        self.board = self.board[:-1] + [ls] + [[1 for x in range(cols)]]

    def check_ok(self, piece, off=(0,0)):
        off_x = off[0]
        off_y = off[1]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                try:
                    if piece[y][x] and self.board[y+off_y][x+off_x]:
                        return False
                except IndexError:
                    return False
        return True

    def clear_rows(self):
        if self.pause or self.gameOver:
            return
        num = 0
        while True:
            for i, row in enumerate(self.board[:-1]):
                if not 0 in row:
                    self.delete_row(i)
                    num += 1
                    break
            else:
                break
        if num:
            pygame.mixer.Sound.play(self.row_sound)
            #x1=pygame.image.load('bangblue.png')
            #Board.__init__(self).screen.fill(x1,(0,0))
        self.score += 100 * num

    def display_matrix(self, matrix, off=(0,0)):
        off_x = off[0]
        off_y = off[1]
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x]:
                    pygame.draw.rect(self.screen, colors[matrix[y][x]],((off_x+x)*blockSize ,
                    (off_y+y)*blockSize, blockSize, blockSize))

    def display_board(self):
        self.display_matrix(self.bg)
        if not self.pause:
            self.display_matrix(self.board)
            self.display_matrix(self.piece, (self.piece_x, self.piece_y))
        else:
            self.big_message("Paused !", (255,255,0), 0, int(-side_space*blockSize/2))
        self.scorer()

        pygame.draw.line(self.screen, colors[2], (cols*blockSize, 0), (cols*blockSize, rows*blockSize), 5)
