import pygame
from global_var import *

class UI(object):
    def __init__(self):
        self.small_font = pygame.font.SysFont(None, small_font_size)
        self.big_font = pygame.font.SysFont(None, big_font_size)
        self.done_sound = pygame.mixer.Sound("sound.wav")
        self.row_sound = pygame.mixer.Sound("row.wav")
        self.image = pygame.image.load("bang.gif")
    def small_message(self, msg, color, y_disp=0, x_disp=0):
        text = self.small_font.render(msg, True, color)
        rect = text.get_rect()
        rect.center = [((cols+side_space)/2)*blockSize + x_disp, (rows/2)*blockSize + y_disp]
        self.screen.blit(text, rect)
        pygame.display.update()

    def big_message(self, msg, color, y_disp=0, x_disp=0):
        text = self.big_font.render(msg, True, color)
        rect = text.get_rect()
        rect.center = [((cols+side_space)/2)*blockSize + x_disp, (rows/2)*blockSize + y_disp]
        self.screen.blit(text, rect)
        pygame.display.update()

    def level_update(self):
        if self.pause or self.gameOver:
            return
        up = 0
        while level_scores[self.level+up] <= self.score:
            up += 1
        self.level += up
        if up:
            pygame.time.set_timer(pygame.USEREVENT+1, 0)
            self.userevent_firetime = int(self.userevent_firetime * 0.65)
            pygame.time.set_timer(pygame.USEREVENT+1, self.userevent_firetime)


    def scorer(self):
        if self.score > self.session_best:
            self.session_best = self.score

        if self.session_best > self.high_score:
            self.high_score = self.session_best

        text = self.small_font.render("Next : ", True, (0,200,200))
        rect = text.get_rect()
        rect.center = [(cols+int(side_space/2))*blockSize, (1)*blockSize]
        self.screen.blit(text, rect)

        self.display_matrix(self.next_piece, (cols-1+side_space/2, 2))

        text = self.small_font.render("Score : " + str(self.score), True, (0,200,200))
        rect = text.get_rect()
        rect.center = [(cols+int(side_space/2))*blockSize, (rows/2 - 1)*blockSize]
        self.screen.blit(text, rect)

        text = self.small_font.render("Level : " + str(self.level), True,(0,200,200))
        rect = text.get_rect()
        rect.center = [(cols+int(side_space/2))*blockSize, (rows/2)*blockSize]
        self.screen.blit(text, rect)

        text = self.small_font.render("Session Best : " + str(self.session_best), True,(0,200,200))
        rect = text.get_rect()
        rect.center = [(cols+int(side_space/2))*blockSize, (rows/2+2)*blockSize]
        self.screen.blit(text, rect)

        text = self.small_font.render("High Score : " + str(self.high_score), True, (0,200,200))
        rect = text.get_rect()
        rect.center = [(cols+int(side_space/2))*blockSize, (rows/2+4)*blockSize]
        self.screen.blit(text, rect)

        pygame.display.update()
        self.level_update()

    def gameOver_screen(self):
        self.screen.fill(colors[0])
        self.big_message("Game Over :(", (200,200, 0), -2*(big_font_size+small_font_size))
        self.small_message("Your Score : " + str(self.score), (200,200, 0), -(small_font_size+big_font_size))
        self.small_message("Session Best Score : " + str(self.session_best), (200,200, 0), -(big_font_size))
        self.small_message("High Score : " + str(self.high_score), (200,200, 0), (small_font_size-big_font_size))
        self.small_message("Q for Quit and C for continue", (200,200, 0), small_font_size)
        pygame.display.update()

    def start_screen(self):
        self.screen.fill(colors[0])
        self.big_message("Tetris :)", (200,0,200), -7*(small_font_size))
        part = int((rows*blockSize)/10)
        self.small_message("left : <- left arrow key",  (200,0,200), -2*(part))
        self.small_message("right : -> right arrow key",  (200,0,200), -1*(part))
        self.small_message("down : v down arrow key",  (200,0,200), 0)
        self.small_message("rotate : ^ up arrow key",   (200,0,200), 1*(part))
        self.small_message("drop : space bar",  (200,0,200), 2*(part))
        self.small_message("pause : p",   (200,0,200), 3*(part))
        self.small_message("Q for Quit and C for continue",  (200,0,200), 4*part)
        #player_image = pygame.image.load("bang.gif")
        #self.image = pygame.image.load("bangblue.png")
        #player_image = pygame.transform.scale(self.image, (100, 100))

        pygame.display.update()
