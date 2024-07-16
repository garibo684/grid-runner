import sys
import pygame as py
from pygame.locals import *

py.init()

    # Variables
# Frames per second
fps = 30

# Colors
blue = (0, 0, 255)
light_blue = (173, 216, 230)
red = (255, 0, 0)
green = (0, 255, 0)
dark_orange = (255, 140, 0)
black = (0, 0, 0)

# Rectangles
rect_position = [151, 151]

# Screen
screen_witdh = 800
screen_height = 600

# Flags
running = True
keys_pressed = {py.K_UP: False, py.K_DOWN: False, py.K_LEFT: False, py.K_RIGHT: False}

    # Display
DISPLAYSURF = py.display.set_mode((screen_witdh, screen_height))
py.display.set_caption('Hello World!')

    # Classes
class Player(py.sprite.Sprite):
    # Constructor
    def __init__(self):
        super().__init__()
        self.image = py.Surface((49, 49))
        self.image.fill(dark_orange)
        self.color = dark_orange
        self.rect = self.image.get_rect()
        self.rect.x = rect_position[0]
        self.rect.y = rect_position[1]
        self.rect.width = 49
        self.rect.height = 49

# Methods
    # Movement
    def move_step(self,key):
        if key == py.K_UP:
            self.rect.y -= 50
        if key == py.K_DOWN:
            self.rect.y += 50
        if key == py.K_LEFT:
            self.rect.x -= 50
        if key == py.K_RIGHT:
            self.rect.x += 50

    def move_cont(self):
        for key in keys_pressed.items():
            if key == py.K_UP:
                self.rect.y -= 50
            if key == py.K_DOWN:
                self.rect.y += 50
            if key == py.K_LEFT:
                self.rect.x -= 50
            if key == py.K_RIGHT:
                self.rect.x += 50

    # Draw gridlines
    def draw_grid(self):
        for x in range(0, screen_witdh, 50):
            py.draw.line(DISPLAYSURF, black, (x, 0), (x, screen_height))
        for y in range(0, screen_height, 50):
            py.draw.line(DISPLAYSURF, black, (0, y), (screen_witdh, y))

    # Draw player rectangle
    def draw_player(self):
        py.draw.rect(DISPLAYSURF, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

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
        if self.rect.x >= screen_witdh - 51:
            self.rect.x = screen_witdh - 49
        if self.rect.y >= screen_height - 51:
            self.rect.y = screen_height - 49
            
    
    # Set Player
player = Player()

    # Main loop
while running:

    # Set frames per second
    py.time.Clock().tick(fps)

    # Fill screen with color
    DISPLAYSURF.fill(light_blue)

    # Player 
    player.draw()
    player.screen_walls()
    player.move_cont()
    # Event loop
    for event in py.event.get():
        # Key events
        if event.type == py.KEYDOWN:
            player.move_step(event.key)
            keys_pressed[event.key] = True
        elif event.type == KEYUP:
            keys_pressed[event.key] = False

        # Quit event
        if event.type == QUIT:
            running = False
            py.quit()
            sys.exit()

    # Update display
    py.display.update()
    
