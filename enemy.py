import pygame
from settings import *
import random
from timer import *
vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        # set ghost starting pos + speed
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.1)

        # set the ghosts individual traits
        self.number = number
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.speed = self.set_speed()

        self.target = None
        # Load Image Files/ Prepare Timers with animations
        self.blinky_up =     pygame.image.load('sounds_images/RedUp1.PNG')
        self.blinky_down =   pygame.image.load('sounds_images/RedDown1.PNG')
        self.blinky_left =   pygame.image.load('sounds_images/RedLeft1.PNG')
        self.blinky_right =  pygame.image.load('sounds_images/RedRight1.PNG')
        self.blinky_up2 =    pygame.image.load('sounds_images/RedUp2.PNG')
        self.blinky_down2 =  pygame.image.load('sounds_images/RedDown2.PNG')
        self.blinky_left2 =  pygame.image.load('sounds_images/RedLeft2.PNG')
        self.blinky_right2 = pygame.image.load('sounds_images/RedRight2.PNG')

        self.pinky_up =      pygame.image.load('sounds_images/PinkUp1.PNG')
        self.pinky_down =    pygame.image.load('sounds_images/PinkDown1.PNG')
        self.pinky_left =    pygame.image.load('sounds_images/PinkLeft1.PNG')
        self.pinky_right =   pygame.image.load('sounds_images/PinkRight1.PNG')
        self.pinky_up2 =     pygame.image.load('sounds_images/PinkUp2.PNG')
        self.pinky_down2 =   pygame.image.load('sounds_images/PinkDown2.PNG')
        self.pinky_left2 =   pygame.image.load('sounds_images/PinkLeft2.PNG')
        self.pinky_right2 =  pygame.image.load('sounds_images/PinkRight2.PNG')

        self.inky_up =       pygame.image.load('sounds_images/CyanUp1.PNG')
        self.inky_down =     pygame.image.load('sounds_images/CyanDown1.PNG')
        self.inky_left =     pygame.image.load('sounds_images/CyanLeft1.PNG')
        self.inky_right =    pygame.image.load('sounds_images/CyanRight1.PNG')
        self.inky_up2 =      pygame.image.load('sounds_images/CyanUp2.PNG')
        self.inky_down2 =    pygame.image.load('sounds_images/CyanDown2.PNG')
        self.inky_left2 =    pygame.image.load('sounds_images/CyanLeft2.PNG')
        self.inky_right2 =   pygame.image.load('sounds_images/CyanRight2.PNG')

        self.clyde_up =      pygame.image.load('sounds_images/OrangeUp1.PNG')
        self.clyde_down =    pygame.image.load('sounds_images/OrangeDown1.PNG')
        self.clyde_left =    pygame.image.load('sounds_images/OrangeLeft1.PNG')
        self.clyde_right =   pygame.image.load('sounds_images/OrangeRight1.PNG')
        self.clyde_up2 =     pygame.image.load('sounds_images/OrangeUp2.PNG')
        self.clyde_down2 =   pygame.image.load('sounds_images/OrangeDown2.PNG')
        self.clyde_left2 =   pygame.image.load('sounds_images/OrangeLeft2.PNG')
        self.clyde_right2 =  pygame.image.load('sounds_images/OrangeRight2.PNG')

        self.blinky_timer_up =    Timer([self.blinky_up,    self.blinky_up2])
        self.blinky_timer_down =  Timer([self.blinky_down,  self.blinky_down2])
        self.blinky_timer_left =  Timer([self.blinky_left, self.blinky_left2])
        self.blinky_timer_right = Timer([self.blinky_right, self.blinky_right2])

        self.pinky_timer_up =     Timer([self.pinky_up,   self.pinky_up2])
        self.pinky_timer_down =   Timer([self.pinky_down,   self.pinky_down2])
        self.pinky_timer_right =  Timer([self.pinky_right, self.pinky_right2])
        self.pinky_timer_left =   Timer([self.pinky_left, self.pinky_left2])

        self.inky_timer_up =      Timer([self.inky_up, self.inky_up2])
        self.inky_timer_down =    Timer([self.inky_down, self.inky_down2])
        self.inky_timer_right =   Timer([self.inky_right, self.inky_right2])
        self.inky_timer_left =    Timer([self.inky_left, self.inky_left2])

        self.clyde_timer_up =     Timer([self.clyde_up, self.clyde_up2])
        self.clyde_timer_down =   Timer([self.clyde_down, self.clyde_down2])
        self.clyde_timer_right =  Timer([self.clyde_right, self.clyde_right2])
        self.clyde_timer_left =   Timer([self.clyde_left, self.clyde_left2])

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        # pygame.draw.circle(self.app.screen, self.color, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)
        # Blit all images to the screen based on the direction they are currently moving 
        # BLIT(image_timer, (x,y))
        x_pixel = self.pix_pos.x - self.app.cell_width // 2
        y_pixel = self.pix_pos.y - self.app.cell_height // 2 - 5

        if self.personality == 'slow':
            if self.direction == vec(0, -1) or self.direction == vec(0, 0):
                self.app.screen.blit(self.blinky_timer_up.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(0, 1):
                self.app.screen.blit(self.blinky_timer_down.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(1, 0):
                self.app.screen.blit(self.blinky_timer_right.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(-1, 0):
                self.app.screen.blit(self.blinky_timer_left.imagerect(), (x_pixel, y_pixel))

        if self.personality == 'speedy':
            if self.direction == vec(0, -1) or self.direction == vec(0, 0):
                self.app.screen.blit(self.pinky_timer_up.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(0, 1):
                self.app.screen.blit(self.pinky_timer_down.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(1, 0):
                self.app.screen.blit(self.pinky_timer_right.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(-1, 0):
                self.app.screen.blit(self.pinky_timer_left.imagerect(), (x_pixel, y_pixel))

        if self.personality == 'random':
            if self.direction == vec(0, -1) or self.direction == vec(0, 0):
                self.app.screen.blit(self.inky_timer_up.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(0, 1):
                self.app.screen.blit(self.inky_timer_down.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(1, 0):
                self.app.screen.blit(self.inky_timer_right.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(-1, 0):
                self.app.screen.blit(self.inky_timer_left.imagerect(), (x_pixel, y_pixel))

        if self.personality == 'scared':
            if self.direction == vec(0, -1) or self.direction == vec(0, 0):
                self.app.screen.blit(self.clyde_timer_up.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(0, 1):
                self.app.screen.blit(self.clyde_timer_down.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(1, 0):
                self.app.screen.blit(self.clyde_timer_right.imagerect(), (x_pixel, y_pixel))

            elif self.direction == vec(-1, 0):
                self.app.screen.blit(self.clyde_timer_left.imagerect(), (x_pixel, y_pixel))

    def get_pix_pos(self):
        # takes our current grid position and translates it to pixels so pygame knows where our unit is
        return vec((self.grid_pos[0] * self.app.cell_width) + BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) + BUFFER // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        x_position = int(self.pix_pos.x + BUFFER // 2) % self.app.cell_width
        y_position = int(self.pix_pos.y + BUFFER // 2) % self.app.cell_height
        if x_position == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if y_position == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.find_pacman(self.target)
        if self.personality == "speedy":
            self.direction = self.find_pacman(self.target)
        if self.personality == "scared":
            self.direction = self.find_pacman(self.target)

    def set_speed(self):
        if self.personality == "speedy":
            speed = 1
        else:
            speed = .5
        return speed

    def set_personality(self):
        if self.number == 0:
            return "random"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "speedy"
        else:
            return "scared"

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(COLS-2, ROWS-2)
            else:
                return vec(1, ROWS-2)

    def get_random_direction(self):
        while True:
            number = random.random()
            if number < 0.25:
                x_dir, y_dir = 1, 0
            elif 0.25 <= number < 0.5:
                x_dir, y_dir = 0, 1
            elif 0.5 <= number < 0.75:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def find_pacman(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x_direction = next_cell[0] - self.grid_pos[0]
        y_direction = next_cell[1] - self.grid_pos[1]
        return vec(x_direction, y_direction)

    def find_next_cell_in_path(self, target):
        path = self.bfs([int(self.grid_pos.x), int(self.grid_pos.y)],
                        [int(target[0]), int(target[1])])
        return path[1]

    def bfs(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbor in neighbors:
                    if 0 <= neighbor[0] + current[0] < len(grid[0]):
                        if 0 <= neighbor[1] + current[1] < len(grid):
                            next_cell = [neighbor[0]+current[0], neighbor[1]+current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
