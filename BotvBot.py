import pygame
import numpy as np
import random
import sys
from GameBot import GameBot

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
shaded_red2 = pygame.Color('#ff5a60')
shaded_blue2 = pygame.Color('#689eb8')
shaded_red = pygame.Color('#e51e2b')
shaded_blue = pygame.Color('#050bab')
light_blue = pygame.Color('#08e8ff')
WIDTH = 1900
HEIGHT = 950

class Game:
    def __init__(self):
        self.size = 19
        self.player1moves = []
        self.player2moves = []
        self.current_player = 1
        self.winner = None
        self.board = []
        for x in range(self.size):
            self.board.append([0] * self.size)
        self.bot = GameBot(self, 1)
        self.bot2 = GameBot(self, 2)

    def get_current_side(self):
        return self.current_player
    def get_point(self, point):
        x, y = point
        if 0 <= x <= self.size and 0 <= y <= self.size:
            return self.board[y][x]

    def reset(self):
        self.player1moves = []
        self.player2moves = []
        self.current_player = 1
        self.winner = None
        self.board = []
        for x in range(self.size):
            self.board.append([0] * self.size)
        self.bot = GameBot(self, 1)
        self.bot2= GameBot(self, 2)

    def step(self):
        pos = [-1, -1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 400 <= pos[0] <= 520 and HEIGHT - 80 <= pos[1] <= HEIGHT - 20:
                    self.reset()
        if self.current_player == 2 and self.winner is None:
            x, y = self.bot2.get_next_move()
            self.board[y][x] = 2
            self.player2moves.append([x, y])
            self.bot.new_move([x, y], 2)
            self.bot2.new_move([x, y], 2)
            self.current_player = 1
        elif self.current_player == 1 and self.winner is None:
            x, y = self.bot.get_next_move()
            self.board[y][x] = 1
            self.player1moves.append([x, y])
            self.bot.new_move([x, y], 1)
            self.bot2.new_move([x, y], 1)
            self.current_player = 2
        '''elif self.current_player == 1:
            if pos != [-1, -1]:
                spotX = int(round(pos[0] / 30.0) - 1)
                spotY = int(round(pos[1] / 30.0) - 1)
                if 0 <= spotX <= self.size and 0 <= spotY <= self.size and self.winner is None:
                    if abs((spotX + 1) * 30 - pos[0]) < 10 and abs((spotY + 1) * 30 - pos[1]) < 10:
                        if self.board[spotY][spotX] == 0:
                            self.player1moves.append([spotX, spotY])
                            self.board[spotY][spotX] = 1
                            self.current_player = 2
                            self.bot.new_move([spotX, spotY], 1)'''
        s = 0
        for row in self.board:
            s += row.count(0)
        if s == 0:
            self.winner = '3'
        if self.check_win(1):
            self.winner = '1'
        elif self.check_win(2):
            self.winner = '2'

    def check_win(self, side=1):
        win_length = 5
        def iter_points(x, y, calc_point):
            i = 0
            while self.get_point(calc_point(x, y, i)) == side:
                i += 1
                if i == win_length:
                    return True
        for y in range(self.size):
            for x in range(self.size):
                # Horizontal
                if x + win_length <= self.size:
                    if iter_points(x, y, lambda x, y, i: (x + i, y)):
                        return True
                # Vertical
                if y + win_length <= self.size:
                    if iter_points(x, y, lambda x, y, i: (x, y + i)):
                        return True
                # Diagonal
                if x + win_length <= self.size and y + win_length <= self.size:
                    # top-left to bottom-right
                    if iter_points(x, y, lambda x, y, i: (x + i, y + i)):
                        return True
                    # bottom-left to top-right
                    if iter_points(x, y, lambda x, y, i: (x + i, y + 4 - i)):
                        return True
        return False

    def render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect 5")
        self.screen.fill(WHITE)#pygame.Color('#DDDDDD'))
        if self.winner is None:
            textsurface = myfont.render('Next Turn: Player ' + str(self.current_player), False, (0, 0, 0))
        elif self.winner == '3':
            textsurface = myfont.render('Tie!', False, (0, 0, 0))
        else:
            textsurface = myfont.render('Player ' + self.winner + ' won!', False, (0, 0, 0))
        self.screen.blit(textsurface, (30, HEIGHT - 86))
        pygame.draw.rect(self.screen, BLACK, (400, HEIGHT - 80, 120, 60), 1)
        textsurface = myfont.render('Reset', False, (0, 0, 0))
        self.screen.blit(textsurface, (420, HEIGHT - 76))
        border = 550
        for x in range(self.size - 1):
            for y in range(self.size - 1):
                swidth = (WIDTH - 2 * border) // (self.size+1)
                sheight = (HEIGHT - 100) // (self.size+1)
                pygame.draw.rect(self.screen, BLACK, (border+swidth * (x + 1), sheight * (y + 1), swidth, sheight), 1)
        for turn in self.player1moves:
            pygame.draw.circle(self.screen, shaded_red, (border + swidth * (turn[0] + 1), sheight * (turn[1] + 1)), min(sheight, swidth) // 3)
        for turn in self.player2moves:
            pygame.draw.circle(self.screen, light_blue, (border + swidth * (turn[0] + 1), sheight * (turn[1] + 1)), min(sheight, swidth) // 3)
        pygame.display.update()

    def step_bot(self, spot):
        s = 0
        for row in self.board:
            s += row.count(0)
        if s < 2:
            self.winner = '3'

        x = spot % self.size
        y = spot // self.size
        while self.winner is None and self.board[y][x] != 0:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
        reward = 0
        if self.winner is None:
            reward = self.bot2.get_score([x, y])
            self.bot.new_move([x, y], 2)
            self.bot2.new_move([x, y], 2)
            self.board[y][x] = 2
            self.player2moves.append([x, y])

            a, b = self.bot.get_next_move()
            self.bot.new_move([a, b], 1)
            self.bot2.new_move([a, b], 1)
            self.board[b][a] = 1
            self.player1moves.append([a, b])

        if self.check_win(1):
            self.winner = '1'
        elif self.check_win(2):
            self.winner = '2'

        return np.reshape(self.board, (1, self.size ** 2)), reward, self.winner

    def reset_bot(self):
        self.player1moves = []
        self.player2moves = []
        self.current_player = 1
        self.winner = None
        self.board = []
        for x in range(self.size):
            self.board.append([0] * self.size)
        self.bot = GameBot(self, 1)
        self.bot2 = GameBot(self, 2)
        return np.reshape(self.board, (1, self.size ** 2))

    def render_text(self):
        for row in self.board:
            print(row)
env = Game()
env.reset()
env.render()
player1wins = 0
player2wins = 0
ties = 0
for x in range(1000):
    while env.winner is None:
        env.step()
        if x % 2 == 0:
            env.render()
        if env.winner == '1':
            player1wins += 1
            print(str(x) + ' Player 1')
        elif env.winner == '2':
            player2wins += 1
            print(str(x) + ' Player 2')
        elif env.winner == '3':
            ties += 1
            print(str(x) + ' Tie')
    env.reset()
    print('Player 1 wins: ' + str(player1wins) + '\tPercentage: ' + str(player1wins / (player1wins + player2wins + ties) * 100))
    print('Player 2 wins: ' + str(player2wins) + '\tPercentage: ' + str(player2wins / (player1wins + player2wins + ties) * 100))
    print('ties: ' + str(ties) + '\tPercentage: ' + str(player2wins / (player1wins + player2wins + ties) * 100))
