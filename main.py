import pygame
from pygame.locals import *
import time
import random

size = 40
bg_col = (110, 110, 5)


class Rat:
    def __init__(self, first):
        self.image = pygame.image.load("Resources/rat.png").convert()
        self.first = first
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.first.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * size
        self.y = random.randint(1, 19) * size


class Snake:
    def __init__(self, first, length):
        self.length = length
        self.first = first
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.first.fill((110, 110, 5))
        for i in range(self.length):
            self.first.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += size
        elif self.direction == 'left':
            self.x[0] -= size
        elif self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(bg_col)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.rat = Rat(self.surface)
        self.rat.draw()

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if (x1 >= x2) and (x1 < x2 + size):
            if (y1 >= y2) and (y1 < y2 + size):
                return True

        return False

    def play(self):
        self.snake.walk()
        self.rat.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.rat.x, self.rat.y):
            self.snake.increase_length()
            self.rat.move()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Collision Occurred")

    def show_game_over(self):
        self.surface.fill(bg_col)
        font = pygame.font.SysFont('aerial', 30)
        line1 = font.render(f"Game is Over:Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again PRESS ENTER. To exit PRESS ESCAPE", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('aerial', 30)
        score = font.render(f"Score:{self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.rat = Rat(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        self.reset()
                        pause = False

                    if not pause:

                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                self.display_score()
                pause = True
                # self.reset()
            time.sleep(0.1)


if __name__ == '__main__':
    game = Game()
    game.run()
