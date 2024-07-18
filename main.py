import sys
from time import sleep
import pygame as py
from random import randint

py.init()

    # Variables
    
# Frames per second
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
dark_orange = (255, 140, 0)
black = (0, 0, 0)

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
    
    # Enemy
enemy_radius = 22
enemy_spawn_counter = 0
enemies = []
enemy_move_counter = 0

# Flags
game_over = False
spawn_flag = True
first_draw = True
ghost_flag = True


    # Display
screen = py.display.set_mode((screen_witdh, screen_height))
py.display.set_caption('Grid Runner')


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

    # Methods

    # Movement
    def move_step(self,key):
        global player_move_counter, enemy_move_counter, direction_flag

        if key == py.K_UP:
            self.rect.y -= step_size
        elif key == py.K_DOWN:
            self.rect.y += step_size
        elif key == py.K_LEFT:
            self.rect.x -= step_size
        elif key == py.K_RIGHT:
            self.rect.x += step_size
        
        player_move_counter += 1
        enemy_move_counter += 1

    # Draw gridlines
    def draw_grid(self):
        for x in range(0, screen_witdh, grid_size[0]):
            py.draw.line(screen, black, (x, 0), (x, screen_height))
        for y in range(0, screen_height, grid_size[1]):
            py.draw.line(screen, black, (0, y), (screen_witdh, y))

    # Draw player rectangle
    def draw_player(self):
        py.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

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

    def draw_enemy(self):
        py.draw.circle(screen, self.color, (self.x, self.y), enemy_radius)
    
    def draw_movement_ghost(self):
        global ghost_flag

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
        ghost_flag = False
        

    def remove_movement_ghost(self):
        global gost_flag

        screen.fill(light_blue)

        # Player 
        player.draw()
        player.screen_walls()

        # Enemy
        for enemy in enemies:
            enemy.draw_enemy()
            enemy.screen_walls()

        ghost_flag = True 

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

    def screen_walls(self):
        if self.x <= 0:
            self.x = grid_size[0] / 2
        if self.y <= 0:
            self.y = grid_size[1] / 2
        if self.x >= screen_witdh - enemy_radius:
            self.x = screen_witdh - (grid_size[0] / 2)
        if self.y >= screen_height - enemy_radius:
            self.y = screen_height - (grid_size[1] / 2)


def spawn_enemy():
    global enemy_spawn_counter, spawn_flag

    rand_row = randint(0, num_rows - 1)
    rand_col = randint(0, num_cols - 1)

    if enemy_spawn_counter == 3:
        spawn_flag = True
        enemy_spawn_counter = 0

    if spawn_flag:
        center_x, center_y = grids[rand_row][rand_col]
        new_enemy = Enemy(center_x, center_y)  # Create a new enemy at the chosen position
        # Assuming you have a list to store enemies
        enemies.append(new_enemy)  # Add the new enemy to the list
        new_enemy.draw_enemy  # Draw all the enemies on the screen
        spawn_flag = False


    # Set Objects
player = Player()

set_grids()

    # Main loop
while not game_over:

    
    # Set frames per second
    clock.tick(fps)

    screen.fill(light_blue)

    # Player 
    player.draw()
    player.screen_walls()

    # Enemy 
    for enemy in enemies:
        enemy.draw_enemy()
        enemy.screen_walls()

    
    # Event loop
    for event in py.event.get():
        # Key events
        if event.type == py.KEYDOWN:

            spawn_enemy()

            player.move_step(event.key)
            
            enemy_move_counter = player_move_counter
            enemy_spawn_counter += 1

            for enemy in enemies:
                enemy.direction = randint(0, 3)
                enemy.draw_movement_ghost()
                enemy.move_enemy()

            if player_move_counter == 2:
                enemy_move_counter = 0
                player_move_counter = 0

            
        

        # Quit event
        if event.type == py.QUIT:
            game_over = True
            py.quit()
            sys.exit()

    # Update display
    py.display.update()
    
