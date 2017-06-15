from board import *
from user_interface import *

class Tetris(Board, UI):

    def __init__(self):

        self.session_best = 0
        high_score_file = open("high_score.txt", "a+")
        self.high_score = high_score_file.read()
        self.high_score = self.high_score if self.high_score else 0
        self.high_score = int(self.high_score)
        high_score_file.close()

        Board.__init__(self)
        UI.__init__(self)

        start = 1
        while start:
            self.start_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.gameExit = True
                        start = 0
                    elif event.key == pygame.K_c:
                        start = 0
                elif event.type == pygame.QUIT:
                    start = 0
                    self.gameExit = True
            self.clock.tick(FPS)

        while not self.gameExit:

            while self.gameOver == True:
                self.gameOver_screen()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.gameOver = False
                            self.gameExit = True
                        elif event.key == pygame.K_c:
                            self.init_new_game()
                            self.gameOver = False
                            self.gameExit = False

                    elif event.type == pygame.QUIT:
                        self.gameOver = False
                        self.gameExit = True
                self.clock.tick(FPS)

            if self.gameExit:
                break

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.drop()
                    elif event.key == pygame.K_LEFT:
                        self.displace(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.displace(1)
                    elif event.key == pygame.K_SPACE:
                        self.continuous_drop()
                    elif event.key == pygame.K_UP:
                        self.rotate()
                    elif event.key == pygame.K_p:
                        self.toggle_pause()
                elif event.type == pygame.USEREVENT + 2:
                    self.push_new_row()
                elif event.type == pygame.QUIT:
                    self.gameOver = False
                    self.gameExit = True

            self.screen.fill(colors[0])
            self.display_board()
            pygame.display.update()
            self.clock.tick(FPS)

        self.conclusion()

    def displace(self, where):
        if self.pause or self.gameOver:
            return
        new_x = self.piece_x + where
        new_y = self.piece_y
        if new_x < 0:
            new_x = 0
        elif new_x > cols - len(self.piece[0]):
            new_x = cols - len(self.piece[0])
        if self.check_ok(self.piece, (new_x, new_y)):
            self.piece_x = new_x

    def rotate_clockwise(self, piece):
        if self.pause or self.gameOver:
            return
        new_piece = []
        for x in range(len(piece[0])):
            ls = []
            for y in range(len(piece)-1, -1, -1):
                ls.append(piece[y][x])
            new_piece.append(ls)
        return new_piece

    def toggle_pause(self):
        self.pause = not self.pause

    def rotate(self):
        if self.pause or self.gameOver:
            return
        new_piece = self.rotate_clockwise(self.piece)
        if self.check_ok(new_piece, (self.piece_x, self.piece_y)):
            self.piece = new_piece

    def continuous_drop(self):
        if self.pause or self.gameOver:
            return
        while not self.drop():
            pass

    def drop(self):
        if self.pause or self.gameOver:
            return
        self.piece_y += 1
        if not self.check_ok(self.piece, (self.piece_x, self.piece_y)):
            self.make_done(self.piece, (self.piece_x, self.piece_y))
            self.new_piece()
            self.clear_rows()
            return True
        return False

    def conclusion(self):
        high_score_file = open("high_score.txt","w+")
        high_score_file.write(str(self.high_score))
        high_score_file.close()

if __name__ == '__main__':
	App = Tetris()
