import sys
from time import sleep
import pygame as py
from random import randint

py.init()

# Variables

# Clock
clock = py.time.Clock()
fps = 30

# Screen
resolution = (800, 600)
screen_witdh = resolution[0]
screen_height = resolution[1]

# Colors
blue = (0, 0, 255)
light_blue = (173, 216, 230)
red = (255, 0, 0)
dark_red = (139, 0, 0)
light_red = (255, 99, 71)
green = (0, 255, 0)
dark_green = (0, 100, 0)
dark_orange = (255, 140, 0)
black = (0, 0, 0)
background_color = (180, 213, 224)

# Objects

# Grid
grid_size = (50, 50)
num_rows = int(screen_height / grid_size[0])
num_cols = int(screen_witdh / grid_size[1])
grids = []

# Player
rect_position = [151, 151]
rect_size = (grid_size[0] - 1, grid_size[1] - 1)
step_size = grid_size[0]
player_move_counter = 0
player_score = 0
high_score = 0

# Enemy
enemy_radius = 22
enemy_spawn_counter = 0
enemies = []
enemy_move_counter = 0
spawn_row, spawn_col = 0, 0

# Flags
game_over = False
spawn_flag = True
first_draw = True
ghost_flag_move = True
ghost_flag_spawn = True
quit_game = False
reset_flag = False
spawn_move_flag = False


# Display
screen = py.display.set_mode((screen_witdh, screen_height))
py.display.set_caption("Grid Runner")


# Functions
def set_grids():
    # Loop through each row
    for row in range(num_rows):
        # Initialize an empty list for this row
        rows = []
        # Loop through each column in the row
        for col in range(num_cols):
            # Calculate the center position for this grid cell
            center_x = (col * grid_size[0]) + (grid_size[0] // 2)
            center_y = (row * grid_size[1]) + (grid_size[1] // 2)
            # Append the center position to the row list
            rows.append((center_x, center_y))
        # Append the row list to the grid_centers list
        grids.append(rows)

    # Classes


# Player
class Player(py.sprite.Sprite):

    # Constructor
    def __init__(self):
        super().__init__()
        self.image = py.Surface((rect_size))
        self.image.fill(dark_orange)
        self.color = dark_orange
        self.rect = self.image.get_rect()
        self.rect.x = rect_position[0]
        self.rect.y = rect_position[1]
        self.rect.width = rect_size[0]
        self.rect.height = rect_size[1]
        self.grid = (0, 0)

    # Methods

    # Movement
    def move_step(self, key):
        global player_move_counter, enemy_move_counter, player_score, high_score

        if key == py.K_UP:
            self.rect.y -= step_size
        elif key == py.K_DOWN:
            self.rect.y += step_size
        elif key == py.K_LEFT:
            self.rect.x -= step_size
        elif key == py.K_RIGHT:
            self.rect.x += step_size

        self.set_grid()

        player_move_counter += 1
        enemy_move_counter += 1
        player_score += 1

        if player_score > high_score:
            high_score = player_score

    # Draw gridlines
    def draw_grid(self):
        for x in range(0, screen_witdh, grid_size[0]):
            py.draw.line(screen, black, (x, 0), (x, screen_height))
        for y in range(0, screen_height, grid_size[1]):
            py.draw.line(screen, black, (0, y), (screen_witdh, y))

    def set_grid(self):
        self.grid = (self.rect.x // grid_size[0], self.rect.y // grid_size[1])

    # Draw player rectangle
    def draw_player(self):
        py.draw.rect(
            screen,
            self.color,
            (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
        )
        self.set_grid()

    # Draw everything
    def draw(self):
        self.draw_grid()
        self.draw_player()

    # Limit player to screen
    def screen_walls(self):
        if self.rect.x <= 0:
            self.rect.x = 1
        if self.rect.y <= 0:
            self.rect.y = 1
        if self.rect.x >= screen_witdh - (grid_size[0] + 1):
            self.rect.x = screen_witdh - rect_size[0]
        if self.rect.y >= screen_height - (grid_size[1] + 1):
            self.rect.y = screen_height - rect_size[1]


# Enemy
class Enemy(py.sprite.Sprite):
    # Constructor
    def __init__(self, spawn_pos_x, spawn_pos_y):
        super().__init__()
        self.image = py.Surface((enemy_radius, enemy_radius), py.SRCALPHA)
        self.color = dark_red
        self.x = spawn_pos_x
        self.y = spawn_pos_y
        self.direction = 0
        self.grid = (0, 0)

    def set_grid(self):
        self.grid = (self.x // grid_size[0], self.y // grid_size[1])

    def draw_enemy(self):
        py.draw.circle(screen, self.color, (self.x, self.y), enemy_radius)
        self.set_grid()

    def draw_movement_ghost(self):
        global ghost_flag_move

        ghost_pos = [self.x, self.y]
        if self.direction == 0:
            ghost_pos[1] = self.y - step_size
        elif self.direction == 1:
            ghost_pos[0] = self.x + step_size
        elif self.direction == 2:
            ghost_pos[1] = self.y + step_size
        elif self.direction == 3:
            ghost_pos[0] = self.x - step_size

        py.draw.circle(screen, red, (ghost_pos), (enemy_radius - 10))
        ghost_flag_move = False

    def remove_movement_ghost(self):
        global gost_flag

        screen.fill(background_color)

        # Player
        player.draw()
        player.screen_walls()

        # Enemy
        for enemy in enemies:
            enemy.draw_enemy()
            enemy.screen_walls()

        ghost_flag_move = True

    def move_enemy(self):
        global enemy_move_counter

        if enemy_move_counter == 2:
            if self.direction == 0:
                self.y -= step_size
            elif self.direction == 1:
                self.x += step_size
            elif self.direction == 2:
                self.y += step_size
            elif self.direction == 3:
                self.x -= step_size

            self.set_grid()

    def screen_walls(self):
        if self.x <= 0:
            self.x = grid_size[0] / 2
        if self.y <= 0:
            self.y = grid_size[1] / 2
        if self.x >= screen_witdh - enemy_radius:
            self.x = screen_witdh - (grid_size[0] / 2)
        if self.y >= screen_height - enemy_radius:
            self.y = screen_height - (grid_size[1] / 2)


def draw_spawn_ghost(ghost_pos):
    global ghost_flag_spawn

    py.draw.circle(screen, dark_green, (ghost_pos), (enemy_radius - 10))
    ghost_flag_spawn = False


def set_spawn_grid():
    global spawn_row, spawn_col

    spawn_row = randint(0, num_rows - 1)
    spawn_col = randint(0, num_cols - 1)

    if spawn_row == player.grid[1] and spawn_col == player.grid[0]:
        spawn_row = randint(0, num_rows - 1)
        spawn_col = randint(0, num_cols - 1)

    for enemy in enemies:
        if spawn_row == enemy.grid[1] and spawn_col == enemy.grid[0]:
            spawn_row = randint(0, num_rows - 1)
            spawn_col = randint(0, num_cols - 1)

    spawn_x, spawn_y = grids[spawn_row][spawn_col]
    return spawn_x, spawn_y


def spawn_enemy(pos):
    global enemy_spawn_counter, spawn_flag, spawn_pos, spawn_move_flag

    if enemy_spawn_counter == 3:
        spawn_flag = True
        enemy_spawn_counter = 0

    if spawn_flag:
        new_enemy = Enemy(pos[0], pos[1])  # Create a new enemy at the chosen position
        # Assuming you have a list to store enemies
        enemies.append(new_enemy)
        new_enemy.draw_enemy  # Draw all the enemies on the screen
        spawn_flag = False
        if enemy_move_counter == 2:
            spawn_move_flag = True

    spawn_pos = set_spawn_grid()


def check_collision():
    player_rect = py.Rect(
        player.rect.x, player.rect.y, player.rect.width, player.rect.height
    )
    for enemy in enemies:
        enemy_rect = py.Rect(
            enemy.x - enemy_radius,
            enemy.y - enemy_radius,
            enemy_radius * 2,
            enemy_radius * 2,
        )
        for another_enemy in enemies:
            if enemy != another_enemy:
                another_enemy_rect = py.Rect(
                    another_enemy.x - enemy_radius,
                    another_enemy.y - enemy_radius,
                    enemy_radius * 2,
                    enemy_radius * 2,
                )
                if enemy_rect.colliderect(another_enemy_rect) or (
                    enemy.grid == another_enemy.grid
                ):
                    enemies.remove(another_enemy)

        if player_rect.colliderect(enemy_rect) or (player.grid == enemy.grid):
            return True

    return False


def display_score():
    font = py.font.SysFont(None, 36)
    score_surf = font.render(f"Score: {player_score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))


def reset_game():
    global game_over, player, enemies, enemy_spawn_counter, player_move_counter, enemy_move_counter, spawn_flag, first_draw, ghost_flag_move, player_score

    game_over = False
    player = Player()
    enemies = []
    enemy_spawn_counter = 0
    player_move_counter = 0
    enemy_move_counter = 0
    player_score = 0
    spawn_flag = True
    first_draw = True
    ghost_flag_move = True


def game_over_screen():
    global game_over, quit_game

    game_over = True

    # Draw the rectangle
    py.draw.rect(
        screen,
        (0, 0, 0),
        (screen_witdh // 4, screen_height // 2 - 100, screen_witdh // 2, 200),
    )
    # Game Over Text
    font = py.font.SysFont(None, 36)

    text_surf = font.render("Game Over!", True, (red))
    play_again_surf = font.render("Play Again? (Y/N)", True, (blue))
    score_surf = font.render(f"    Score: {player_score}", True, (dark_orange))
    high_score_surf = font.render(f"    High Score: {high_score}", True, (green))

    screen.blit(text_surf, (screen_witdh // 4 + 50, screen_height // 2 - 80))
    screen.blit(score_surf, (screen_witdh // 4 + 50, screen_height // 2))
    screen.blit(high_score_surf, (screen_witdh // 4 + 50, screen_height // 2 - 35))
    screen.blit(play_again_surf, (screen_witdh // 4 + 50, screen_height // 2 + 50))

    # Set Objects


player = Player()

set_grids()
spawn_pos = set_spawn_grid()
draw_spawn_ghost(spawn_pos)

# Main loop
while not quit_game:

    # Set frames per second
    clock.tick(fps)

    screen.fill(background_color)

    # Player
    player.draw()
    player.screen_walls()

    # Enemy
    for enemy in enemies:
        enemy.draw_enemy()
        enemy.screen_walls()
        if player_move_counter == 1:
            enemy.draw_movement_ghost()

    if enemy_spawn_counter == 3 or first_draw:
        draw_spawn_ghost(spawn_pos)

    collision = check_collision()
    if collision:
        game_over_screen()

    display_score()

    # Event loop
    for event in py.event.get():
        # Key events
        if event.type == py.KEYDOWN:

            if not game_over:
                first_draw = False

                player.move_step(event.key)

                spawn_enemy(spawn_pos)

                enemy_move_counter = player_move_counter
                enemy_spawn_counter += 1
                ghost_flag_spawn = True

                for enemy in enemies:
                    if player_move_counter == 1:
                        enemy.direction = randint(0, 3)

                    if spawn_move_flag and enemy == enemies[-1]:
                        spawn_move_flag = False
                    else:
                        enemy.move_enemy()

                if player_move_counter == 2:
                    enemy_move_counter = 0
                    player_move_counter = 0
            else:
                if event.key == py.K_y:
                    reset_game()
                elif event.key == py.K_n:
                    quit_game = True

        # Quit event
        if event.type == py.QUIT or quit_game:
            game_over = False
            quit_game = False
            py.quit()
            sys.exit()

    # Update display
    py.display.update()
