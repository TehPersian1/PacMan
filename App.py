import sys
from player import *
from enemy import *

pygame.init()
vec = pygame.math.Vector2


def draw_text(words, screen, pos, size, color, font_name):
    # centers start screen text and assigns font/color
    font = pygame.font.SysFont(font_name, size)
    text = font.render(words, False, color)
    text_size = text.get_size()
    pos[0] = pos[0] - text_size[0] // 2
    pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)


class App:
    def __init__(self):
        # initialize game state
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.background = None
        # initialize Sound Bytes
        self.bgm = pygame.mixer.Sound('sounds_images/pacman_beginning.wav')
        self.death_sound = pygame.mixer.Sound('sounds_images/pacman_death.wav')
        self.eat_sound = pygame.mixer.Sound('sounds_images/pacman_chomp.wav')

        # create player/enemy lists
        self.player_pos = None
        self.enemies = []
        self.enemy_pos = []

        # split up our window into a grid of specific sized cells
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS

        # create walls/coins lists
        self.walls = []
        self.coins = []
        self.portals = []
        self.power_pills = []

        # Load initial game procedures
        self.load()
        self.player = Player(self, vec(self.player_pos))
        self.load_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over' or self.state == 'game over new score':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ##########################################################
    #                    HELPER FUNCTIONS                    #
    #  These Functions use elements from all the classes     #
    #  we have created to pull the game together. creating   #
    # elements to draw to the screen as well as loading      #
    # the game files and creating the first game-state       #
    ##########################################################

    def load(self):
        # LOAD MAZE IMAGE AND SCALE TO WINDOW SIZE
        self.background = pygame.image.load('sounds_images/Maze.jpg')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        self.bgm.play(0)
        # Opening Walls File and creating walls list w/ Coordinates
        with open('walls.txt', 'r') as file:
            for index_Y, line in enumerate(file):
                for index_X, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(index_X, index_Y))
                    elif char == 'C':
                        self.coins.append(vec(index_X, index_Y))
                    elif char == 'P':
                        self.player_pos = [index_X, index_Y]
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append([index_X, index_Y])
                    elif char == 'T':
                        self.portals.append(vec(index_X, index_Y))
                    elif char == 'U':
                        self.power_pills.append((vec(index_X, index_Y)))

    def load_enemies(self):
        for index, pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, vec(pos), index))

    def draw_grind(self):
        # For Development Purposes, Will be disabled when turned in
        cw = self.cell_width
        ch = self.cell_height
        bg = self.background
        for x in range(WIDTH // cw):
            pygame.draw.line(bg, GRAY, (x * cw, 0), (x * cw, HEIGHT))
        for x in range(HEIGHT // ch):
            pygame.draw.line(bg, GRAY, (0, x * ch), (WIDTH, x * ch))
        # Colors in all of the "wall" grids
        for wall in self.walls:
            pygame.draw.rect(bg, (112, 55, 163), (wall.x * cw, wall.y * ch, cw, ch))
        # Colors in all of the "coin" grids
        for coin in self.coins:
            pygame.draw.rect(bg, (167, 179, 34), (coin.x * cw, coin.y * ch, cw, ch))

    def reset(self):
        # Reset Player Lives/Score - Move player/enemies back to starting positions
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        # Reset Coins/pills on the maze
        self.coins = []
        self.power_pills = []
        with open('walls.txt', 'r') as file:
            for index_Y, line in enumerate(file):
                for index_X, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(index_X, index_Y))
                    elif char == 'U':
                        self.power_pills.append(vec(index_X, index_Y))
        self.state = 'playing'
        self.bgm.play(0)

    ###############################################################
    #                        START FUNCTIONS                      #
    # These Functions are responsible for the interactions with   #
    # The Player and the start screen, such as showing highscores #
    # and starting the actual Game with the space                 #
    ###############################################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        draw_text('PUSH SPACE TO START', self.screen, [WIDTH // 2, HEIGHT - 150],
                  START_TEXT_SIZE, START_ORANGE, START_FONT)
        draw_text('PUSH ESC TO QUIT', self.screen, [WIDTH // 2, HEIGHT - 125],
                  START_TEXT_SIZE, START_ORANGE, START_FONT)
        draw_text('P', self.screen, [55, HEIGHT // 10],
                  PACMAN_SIZE, START_PEACH, PACMAN_FONT)
        draw_text('A', self.screen, [137, HEIGHT // 10],
                  PACMAN_SIZE, START_PEACH, PACMAN_FONT)
        draw_text('M', self.screen, [343, HEIGHT // 10],
                  PACMAN_SIZE, START_PEACH, PACMAN_FONT)
        draw_text('A', self.screen, [450, HEIGHT // 10],
                  PACMAN_SIZE, START_PEACH, PACMAN_FONT)
        draw_text('N', self.screen, [555, HEIGHT // 10],
                  PACMAN_SIZE, START_PEACH, PACMAN_FONT)
        image = pygame.image.load('sounds_images/Title_pac.jpg')
        image = pygame.transform.scale(image, (MAZE_WIDTH // TITLE_SIZE, MAZE_HEIGHT // TITLE_SIZE))
        self.screen.blit(image, (190, HEIGHT // 10))
        draw_text("Current HighScore: {}".format(self.player.high_score), self.screen, [WIDTH // 2, HEIGHT // 2 + 260],
                  35, WHITE, START_FONT)
        pygame.display.update()

    #################################################################
    #                       PLAYING FUNCTIONS                       #
    # These Functions control the actual Game-play, from drawing    #
    # images to updating scores, this is the main portion of the    #
    # Game Loop                                                     #
    #################################################################
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (BUFFER // 2, BUFFER // 2))
        # self.draw_grind() # Used for Development, you can uncomment
        # to see how the Walls.txt is translated into coins/walls
        self.draw_coins()
        draw_text('HIGH SCORE: {}'.format(self.player.high_score),
                  self.screen, [485, 10], 15, WHITE, START_FONT)
        draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                  self.screen, [95, 10], 15, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def draw_coins(self):
        cw = self.cell_width
        ch = self.cell_height
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE,
                               (int(coin.x * cw) + cw // 2 + BUFFER // 2,
                                int(coin.y * ch) + ch // 2 + BUFFER // 2), 5)
        for pill in self.power_pills:
            pygame.draw.circle(self.screen, WHITE, (int(pill.x * cw) + cw // 2 + BUFFER // 2,
                                                    int(pill.y * ch) + ch // 2 + BUFFER // 2), 9)

    def remove_life(self):
        self.player.lives -= 1
        self.death_sound.play(0)
        if self.player.lives == 0:
            if self.player.current_score > self.player.high_score:
                self.player.high_score = self.player.current_score
                self.state = "game over new score"
            else:
                self.state = "game over"

        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    ####################################################
    #               GAME OVER FUNCTIONS                #
    # These functions control what happens in the app  #
    # after the player has run out of lives            #
    ####################################################
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_draw(self):
        self.screen.fill(BLACK)
        draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 92, RED, "arial")
        draw_text(QUIT_TEXT, self.screen, [WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), "arial")
        if self.state == "game over new score":
            draw_text(SCORE_TEXT, self.screen, [WIDTH // 2, HEIGHT // 1.2], 30, PLAYER_COLOR, "arial")
            draw_text("New Score: {}".format(self.player.high_score), self.screen, [WIDTH // 2, HEIGHT // 1.2 + 40],
                      30, RED, "arial")
        draw_text(RESTART_TEXT, self.screen, [WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190), "arial")
        pygame.display.update()

    def game_over_update(self):
        pass
