import pygame, sys, random
from pygame.math import Vector2


class FRUIT:
    # create x and y position
    # draw a square
    def __init__(self):
        self.random_fruit()

    # creat a rect for the fruit
    # draw the rect
    def draw_fruit(self):
        x_position = int(self.position.x * cell_size)
        y_position = int(self.position.y * cell_size)
        fruit_rect = pygame.Rect(x_position, y_position, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def random_fruit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)


class SNAKE:
    # create the body of the snake, will start in same spot every time
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    # draw the snake by creating rect and draw its position
    def draw_snake(self):
        for block in self.body:
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            block_rect = pygame.Rect(x_position, y_position, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def ate_food(self):
        self.new_block = True


class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()

    def update(self):
        self.snake.move_snake()
        self.collision_checker()
        self.fail_checker()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    
    def collision_checker(self):
        # compare the fruit position with the head of the snake
        if self.fruit.position == self.snake.body[0]:
            # we want to reposition the fruit
            self.fruit.random_fruit()
            # add another block to the snake
            self.snake.ate_food()

    def fail_checker(self):
        # check if snake is outside of screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake_died()
        # check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake_died()

    def snake_died(self):
        pygame.quit()
        sys.exit()



# set up all pygame requirements
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

# Update the screen every 150ms to move snake
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()

    # draw all our elements
    pygame.display.update()
    clock.tick(60)