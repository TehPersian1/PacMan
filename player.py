from settings import *
import pygame
from timer import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.high_score = 0
        self.speed = 1
        self.lives = 3
        self.lives_image = pygame.image.load('sounds_images/Title_pac.jpg')
        self.lives_image = pygame.transform.scale(self.lives_image, (MAZE_WIDTH//COLS, MAZE_HEIGHT//ROWS))
        self.starting_pos = [pos.x, pos.y]

        # Load Pac Man Images
        self.left0 = pygame.image.load('sounds_images/PacLeft0.jpg')
        self.left1 = pygame.image.load('sounds_images/PacLeft1.jpg')
        self.left2 = pygame.image.load('sounds_images/PacLeft2.jpg')
        self.left3 = pygame.image.load('sounds_images/PacLeft3.jpg')
        self.left_timer = Timer([self.left0, self.left1, self.left2, self.left3])

        self.right0 = pygame.image.load('sounds_images/PacRight0.jpg')
        self.right1 = pygame.image.load('sounds_images/PacRight1.jpg')
        self.right2 = pygame.image.load('sounds_images/PacRight2.jpg')
        self.right3 = pygame.image.load('sounds_images/PacRight3.jpg')
        self.right_timer = Timer([self.right0, self.right1, self.right2, self.right3])

        self.up0 = pygame.image.load('sounds_images/PacUp0.jpg')
        self.up1 = pygame.image.load('sounds_images/PacUp1.jpg')
        self.up2 = pygame.image.load('sounds_images/PacUp2.jpg')
        self.up3 = pygame.image.load('sounds_images/PacUp3.jpg')
        self.up_timer = Timer([self.up0, self.up1, self.up2, self.up3])

        self.down0 = pygame.image.load('sounds_images/PacDown0.jpg')
        self.down1 = pygame.image.load('sounds_images/PacDown1.jpg')
        self.down2 = pygame.image.load('sounds_images/PacDown2.jpg')
        self.down3 = pygame.image.load('sounds_images/PacDown3.jpg')
        self.down_timer = Timer([self.down0, self.down1, self.down2, self.down3])

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        if self.on_portal():
            self.teleport()
        if self.on_power_pill():
            self.eat_pill()

        # setting Grid Position[x][y] = to pixel position (Tracking Pacman on the grid)
        self.grid_pos[0] = (self.pix_pos[0] - BUFFER+self.app.cell_width//2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - BUFFER+self.app.cell_height//2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # pygame.draw.circle(self.app.screen, PLAYER_COLOR,
        #                    (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)
        center = (int(self.pix_pos.x-self.app.cell_width // 2), int(self.pix_pos.y-self.app.cell_height // 2))

        if self.direction == vec(1, 0) or self.direction == vec(0, 0):
            self.app.screen.blit(self.right_timer.imagerect(), center)
        elif self.direction == vec(-1, 0):
            self.app.screen.blit(self.left_timer.imagerect(), center)
        elif self.direction == vec(0, 1):
            self.app.screen.blit(self.down_timer.imagerect(), center)
        elif self.direction == vec(0, -1):
            self.app.screen.blit(self.up_timer.imagerect(), center)
        # draw the lives
        for x in range(self.lives):
            self.app.screen.blit(self.lives_image, (15 + 30*x, HEIGHT-20))

        # Draw a Rectangle that tracks the player's current grid position
        # pygame.draw.rect(self.app.screen, RED,
        # (self.grid_pos[0]*self.app.cell_width+BUFFER//2,
        # self.grid_pos[1]*self.app.cell_height+BUFFER//2,
        # self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width) + BUFFER//2 + self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) + BUFFER//2 + self.app.cell_height//2)

    def time_to_move(self):
        # This Function checks to see if Pac Man is at the center of a grid,
        # if he is, he can move to another tile and accept user input, if not he must finish moving
        pos_x = self.pix_pos.x + BUFFER // 2
        pos_y = self.pix_pos.y + BUFFER // 2
        cw = self.app.cell_width
        ch = self.app.cell_height
        if int(pos_x) % cw == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(pos_y) % ch == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def can_move(self):
        # checks for wall collisions with pacman
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    def on_coin(self):
        # checks if the player is on a grid with a coin ; returns true
        pos_x = self.pix_pos.x + BUFFER // 2
        pos_y = self.pix_pos.y + BUFFER // 2
        cw = self.app.cell_width
        ch = self.app.cell_height
        if self.grid_pos in self.app.coins:
            if int(pos_x) % cw == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(pos_y) % ch == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def on_portal(self):
        pos_x = self.pix_pos.x + BUFFER // 2
        pos_y = self.pix_pos.y + BUFFER // 2
        cw = self.app.cell_width
        ch = self.app.cell_height

        if self.grid_pos in self.app.portals:
            if int(pos_x) % cw == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(pos_y) % ch == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def teleport(self):
        if self.on_portal():
            if self.grid_pos == self.app.portals[0]:
                self.grid_pos = self.app.portals[1] + vec(-1, 0)
            elif self.grid_pos == self.app.portals[1]:
                self.grid_pos = self.app.portals[0] + vec(1, 0)
            elif self.grid_pos == self.app.portals[2]:
                self.grid_pos = self.app.portals[3] + vec(-1, 0)
            elif self.grid_pos == self.app.portals[3]:
                self.grid_pos = self.app.portals[2] + vec(1, 0)

        self.pix_pos = self.get_pix_pos()
        self.draw()

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 10
        self.app.eat_sound.play(0, 700)

    def eat_pill(self):
        self.app.power_pills.remove(self.grid_pos)

    def on_power_pill(self):
        pos_x = self.pix_pos.x + BUFFER // 2
        pos_y = self.pix_pos.y + BUFFER // 2
        cw = self.app.cell_width
        ch = self.app.cell_height

        if self.grid_pos in self.app.power_pills:
            if int(pos_x) % cw == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(pos_y) % ch == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False
