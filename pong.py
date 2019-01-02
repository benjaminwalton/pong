import pygame
import sys
import random
import time

# Game settings
screen_width = 1200
screen_height = 780
bg_color = (0, 0, 0)
speed_factor = 10
ball_speed  = 5

class Player():
    """Player paddle"""
    score = 0
    def __init__(self, screen, player_num):
        self.screen = screen
        self.player_num = player_num

        # Set paddle size and create pygame surface
        self.width=15
        self.height=75
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start paddle in the middle of the screen
        # x position is different depending on player number
        if self.player_num == 1:
            self.rect.centerx = 50
            self.rect.centery = 390
        elif self.player_num == 2:
            self.rect.centerx = 1150
            self.rect.centery = 390

        # Store value for the paddle center
        self.center = float(self.rect.centery)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update paddle position based on movement flag"""
        if self.moving_up and self.rect.top > self.screen_rect.top :
            self.center -= speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center += speed_factor

        # Update rect from self.center
        self.rect.centery = self.center

    def blitme(self):
        """Draw paddle at current position"""
        self.screen.blit(self.image, self.rect)

class Ball():
    """Class to initialize ball and update position"""
    def __init__(self, screen, player1, player2, boing, doh):
        self.dir_x = random.choice([1,-1]) 
        self.dir_y = random.choice([1,-1]) 
        self.boing = boing
        self.doh = doh

        self.screen = screen
        self.width=15
        self.height=15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)
        self.player1 = player1.rect
        self.player2 = player2.rect

    def update(self):
        """Update ball on the screen"""
        if self.rect.top <= self.screen_rect.top or self.rect.bottom >= self.screen_rect.bottom:
            self.dir_y = self.dir_y * -1
            pygame.mixer.Sound.play(self.boing)
        if self.rect.right == self.player2.left and self.rect.bottom >= self.player2.top and self.rect.top <= self.player2.bottom:
            self.dir_x = self.dir_x * -1
            pygame.mixer.Sound.play(self.boing)
        if self.rect.left == self.player1.right and self.rect.bottom >= self.player1.top and self.rect.top <= self.player1.bottom:
            self.dir_x = self.dir_x * -1
            pygame.mixer.Sound.play(self.boing)

        self.centerx -= (self.dir_x * ball_speed)
        self.centery += (self.dir_y * ball_speed)

        # Update rect from self.center
        self.rect.centery = self.centery
        self.rect.centerx = self.centerx

    def score(self, player1, player2):
        """Track score changes"""
        if self.rect.left > self.screen_rect.right:
            pygame.mixer.Sound.play(self.doh)
            player1.score += 1
            return(True)
        if self.rect.right < self.screen_rect.left:
            pygame.mixer.Sound.play(self.doh)
            player2.score += 1
            return(True)
        return(False)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

def check_keydown_events(event, player):
    """Check for key presses. W/S for player one, up/down for player 2"""
    if player.player_num == 2:
        if event.key == pygame.K_UP:
            player.moving_up = True
        if event.key == pygame.K_DOWN:
            player.moving_down = True
    elif player.player_num == 1:
        if event.key == pygame.K_w:
            player.moving_up = True
        if event.key == pygame.K_s:
            player.moving_down = True

def check_keyup_events(event, player):
    """Respond to key releases"""
    if player.player_num == 2:
        if event.key == pygame.K_UP:
            player.moving_up = False
        if event.key == pygame.K_DOWN:
            player.moving_down = False
    elif player.player_num == 1:
        if event.key == pygame.K_w:
            player.moving_up = False
        if event.key == pygame.K_s:
            player.moving_down = False

def update_screen(screen, player1, player2, ball, myFont):
    """Update images on the screen"""
    # Redraw screen
    screen.fill(bg_color)
    player1.blitme()
    player2.blitme()
    ball.blitme()

    # Draw score to screen
    score = update_score(player1, player2, myFont)
    screen.blit(score[0], (300, 20))
    screen.blit(score[1], (900, 20))

    if player1.score == 11:
        screen.blit(score[0], (300, 20))
        message = myFont.render("Player 1 Wins!", 1, (255, 255, 255))
        screen.blit(message, (300, 390))

    if player2.score == 11:
        screen.blit(score[1], (900, 20))
        message = myFont.render("Player 2 Wins!", 1, (255, 255, 255))
        screen.blit(message, (650, 390))

    pygame.draw.rect(screen, (255, 255, 255), (600, 0, 7, screen_height), 0)

    # Make most recently drawn screen visible
    pygame.display.flip()

def check_events(player1, player2):
    """Respond to keypresses and mouse clicks"""
    for event in pygame.event.get():
        # Quit game if window is closed
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player1)
            check_keydown_events(event, player2)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player1)
            check_keyup_events(event, player2)

def update_score(player1, player2, myFont):
    score1 = myFont.render(str(player1.score), 1, (255, 255, 255))
    score2 = myFont.render(str(player2.score), 1, (255, 255, 255))
    return score1, score2

def run_game():

    # Initialize game, settings, and screen
    pygame.init()
    boing = pygame.mixer.Sound("sm64_mario_boing.wav")
    doh = pygame.mixer.Sound("sm64_mario_doh.wav")
    screen = pygame.display.set_mode(
        (screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # Start music
    pygame.mixer.music.load('05 Super Mario 64 Main Theme.mp3')
    pygame.mixer.music.play(-1)

    myFont = pygame.font.SysFont("Times New Roman", 50)
    player1 = Player(screen, 1)
    player2 = Player(screen, 2)
    ball = Ball(screen, player1, player2, boing, doh)

    while True:
        ball = Ball(screen, player1, player2, boing, doh)
        score = False
        while not score:
            check_events(player1, player2)
            player1.update()
            player2.update()
            ball.update()
            update_screen(screen, player1, player2, ball, myFont)
            score = ball.score(player1, player2)
        
        if player1.score == 11 or player2.score == 11:
            pygame.mixer.music.stop()
            celebrate = pygame.mixer.Sound("sm64_here_we_go.wav")
            thanks = pygame.mixer.Sound("sm64_mario_thank_you.wav")
            pygame.mixer.Sound.play(celebrate)
            pygame.mixer.Sound.play(thanks)

            while True:
                check_events(player1, player2)
                player1.update()
                player2.update()

                update_screen(screen, player1, player2, ball, myFont)       
        time.sleep(2)
        
run_game()