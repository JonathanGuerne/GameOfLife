import pygame

import numpy as np

from utils import get_neighboors, color_from_code, get_mean_color_code

import time


class GameOfLife():

    def __init__(self, width=800, height=800, res_x=50, res_y=50):

        self.screen = None
        self.resolution = None

        self.width = width
        self.height = height

        self.resolution = (res_y, res_x)

        self.cell_width = None
        self.cell_height = None

        self.game_board = None

        self.init_screen()
        self.init_world()
        self.random_start()

    def init_screen(self):

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height))

    def init_world(self):

        self.cell_width = self.width / self.resolution[1]
        self.cell_height = self.height / self.resolution[0]

        self.game_board = np.zeros(self.resolution)

    def random_start(self):

        for i in range(self.resolution[1]):
            for j in range(self.resolution[0]):

                if np.random.random() > 0.85:
                    self.game_board[j, i] = np.random.randint(0, 1000)

    def apply_rules(self):

        prev_state = np.copy(self.game_board)

        for x in range(self.resolution[1]):
            for y in range(self.resolution[0]):

                cell_state = prev_state[y, x]
                neighboors = get_neighboors(prev_state, x, y)
                n_neighboors = len(neighboors)

                if cell_state == 0 and n_neighboors == 3:
                    self.game_board[y, x] = get_mean_color_code(neighboors)

                elif cell_state > 0 and (n_neighboors < 2 or n_neighboors > 3):
                    self.game_board[y, x] = 0

    def __draw(self, screen, draw_lines=False):

        screen.fill((255, 255, 255))

        for i in range(self.resolution[1]):
            for j in range(self.resolution[0]):

                if self.game_board[j, i] > 0:

                    c = self.game_board[j, i]
                    color = color_from_code(c)

                    pygame.draw.rect(screen,
                                     color,
                                     (int(i * self.cell_width),
                                      int(j * self.cell_height),
                                      int(self.cell_width),
                                         int(self.cell_height)))
        if draw_lines:

            for i in range(self.resolution[1]):

                pygame.draw.line(screen, (0, 0, 0), (0, int(i * self.cell_width)),
                                 (int(self.width), int(i * self.cell_width)), 1)

            for j in range(self.resolution[0]):

                pygame.draw.line(screen, (0, 0, 0), (int(j * self.cell_height), 0),
                                 (int(j * self.cell_height), int(self.height)), 1)

    def change_cell(self, x, y):

        if self.game_board[y, x] > 0:
            self.game_board[y, x] = 0
        else:
            self.game_board[y, x] = np.random.randint(0, 1000)

    def game_loop(self):

        if not self.screen:
            self.init_screen()

        # self.__draw(self.screen)

        run = True
        line = False
        is_apply_rules = False

        sleep_time = 50

        pygame.key.set_repeat(1)

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    x, y = pygame.mouse.get_pos()
                    x = int(x // self.cell_width)
                    y = int(y // self.cell_height)

                    self.change_cell(x, y)

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_l:
                        line = not line
                    elif event.key == pygame.K_q:
                        run = False
                    elif event.key == pygame.K_s:
                        is_apply_rules = not is_apply_rules
                    elif event.key == pygame.K_LEFT:
                        sleep_time = sleep_time + 10 if sleep_time < 10000 else sleep_time
                    elif event.key == pygame.K_RIGHT:
                        sleep_time = sleep_time - 10 if sleep_time >= 10 else sleep_time
                    elif event.key == pygame.K_a:
                        self.init_world()

            t1 = time.time()

            self.__draw(self.screen, draw_lines=line)

            if is_apply_rules:
                self.apply_rules()

            t_tot = time.time() - t1

            pygame.time.delay(sleep_time)

            pygame.display.update()


if __name__ == "__main__":

    gof = GameOfLife()
    gof.game_loop()
