import pygame, sys, random
from pygame.math import Vector2


class CUP:
    # create x and y position
    # draw a square
    def __init__(self):
        self.random_cup()

    # creat a rect for the cup
    # draw the rect
    def draw_cup(self):
        x_position = int(self.position.x * cell_size)
        y_position = int(self.position.y * cell_size)
        cup_rect = pygame.Rect(x_position, y_position, cell_size, cell_size)
        screen.blit(cup_image, cup_rect)
        #pygame.draw.rect(screen, (126, 166, 114), cup_rect)

    def random_cup(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)


class SNAKE:
    # create the body of the snake, will start in same spot every time
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_body_piece = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.snake_sound = pygame.mixer.Sound('Sound/snake_sound.wav')

    # draw the snake by creating rect and draw its position
    def draw_snake(self):
        # update snake body directions
        self.update_snake_head()
        self.update_snake_tail()

        for index, body_piece in enumerate(self.body):
            # we still need a rect for the positioning
            x_position = int(body_piece.x * cell_size)
            y_position = int(body_piece.y * cell_size)
            body_rect = pygame.Rect(x_position, y_position, cell_size, cell_size)

            # head of snake
            if index == 0:
                screen.blit(self.head, body_rect)
            # tail of snake
            elif index == len(self.body) - 1:
                screen.blit(self.tail, body_rect)
            # body of snake
            else:
                prev_body_piece = self.body[index + 1] - body_piece
                next_body_piece = self.body[index - 1] - body_piece

                # vertical body piece
                if prev_body_piece.x == next_body_piece.x:
                    screen.blit(self.body_vertical, body_rect)
                # horizontal body piece
                elif prev_body_piece.y == next_body_piece.y:
                    screen.blit(self.body_horizontal, body_rect)
                # corner body pieces
                else:
                    # top left corner
                    if prev_body_piece.x == -1 and next_body_piece.y == -1 or prev_body_piece.y == -1 and next_body_piece.x == -1:
                        screen.blit(self.body_tl, body_rect)
                    # bottom left corner
                    elif prev_body_piece.x == -1 and next_body_piece.y == 1 or prev_body_piece.y == 1 and next_body_piece.x == -1:
                        screen.blit(self.body_bl, body_rect)
                    # top right corner
                    elif prev_body_piece.x == 1 and next_body_piece.y == -1 or prev_body_piece.y == -1 and next_body_piece.x == 1:
                        screen.blit(self.body_tr, body_rect)
                    # bottom right corner
                    elif prev_body_piece.x == 1 and next_body_piece.y == 1 or prev_body_piece.y == 1 and next_body_piece.x == 1:
                        screen.blit(self.body_br, body_rect)

    def update_snake_head(self):
        difference = self.body[1] - self.body[0]

        if difference == Vector2(1, 0):
            self.head = self.head_left
        elif difference == Vector2(-1, 0):
            self.head = self.head_right
        elif difference == Vector2(0, 1):
            self.head = self.head_up
        elif difference == Vector2(0, -1):
            self.head = self.head_down

    def update_snake_tail(self):
        difference = self.body[len(self.body) - 2] - self.body[len(self.body) - 1]

        if difference == Vector2(1, 0):
            self.tail = self.tail_left
        elif difference == Vector2(-1, 0):
            self.tail = self.tail_right
        elif difference == Vector2(0, 1):
            self.tail = self.tail_up
        elif difference == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_body_piece == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_body_piece = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def ate_food(self):
        self.new_body_piece = True

    def play_sound(self):
        self.snake_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class MAIN:
    def __init__(self):
        self.cup = CUP()
        self.snake = SNAKE()

    def update(self):
        self.snake.move_snake()
        self.collision_checker()
        self.fail_checker()

    def draw_elements(self):
        self.grass()
        self.cup.draw_cup()
        self.snake.draw_snake()
        self.score()
    
    def collision_checker(self):
        # compare the cup position with the head of the snake
        if self.cup.position == self.snake.body[0]:
            # we want to reposition the cup
            self.cup.random_cup()
            # add another block to the snake
            self.snake.ate_food()
            # play sound when eating
            self.snake.play_sound()
        
        # make sure that cup never lands on snake body
        for body_piece in self.snake.body[1:]:
            if body_piece == self.cup.position:
                self.cup.random_cup()

    def fail_checker(self):
        # check if snake is outside of screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake_died()

        # check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake_died()

    def snake_died(self):
        self.snake.reset()

    def grass(self):
        color = (255, 212, 59)

        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, grass_rect)

    def score(self):
        text = str(len(self.snake.body) - 3)
        surface = font.render(text, True, (0, 0, 0))
        x = int(cell_size * cell_number - 40)
        y = 40
        score_rect = surface.get_rect(center = (x, y))
        cup_rect = cup_image.get_rect(midright = (score_rect.left - 2, score_rect.centery))
        background_rect = pygame.Rect(cup_rect.left - 6, cup_rect.top - 4, cup_rect.width + score_rect.width + 14, cup_rect.height + 8)

        pygame.draw.rect(screen, (255, 255, 255), background_rect)
        screen.blit(surface, score_rect)
        screen.blit(cup_image, cup_rect)
        pygame.draw.rect(screen, (0, 0, 0), background_rect, 2)


# set up all pygame requirements
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 16
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
cup_image = pygame.image.load('Graphics/java_black.png').convert_alpha()
font = pygame.font.Font('Font/snake_font.ttf', 25)

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

    screen.fill((255, 232, 115))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
