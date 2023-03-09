import pygame, sys
import random

# class Block(pygame.sprite.Sprite):

# class Player(Block):

# class Ball(Block):

# class Opponent(Block):

# class GameManager(Block):

def ball_animation():
    global ball_speed_x, ball_speed_y, player_points, opponent_points, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_points += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_points += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1


def draw_score():
    score_text = str(opponent_points)
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    score_surface = font.render(score_text, True, (0, 0, 0))
    score_x = screen_width / 4
    score_y = screen_height - 50
    score_rect = score_surface.get_rect(center = (score_x, score_y))
    
    pygame.draw.rect(screen, ((255, 255, 255)), score_rect)
    screen.blit(score_surface, score_rect)
    pygame.draw.rect(screen, (0, 0, 0), score_rect, 1)

    score_text = str(player_points)
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    score_surface = font.render(score_text, True, (0, 0, 0))
    score_x = (screen_width / 4) * 3
    score_y = screen_height - 50
    score_rect = score_surface.get_rect(center = (score_x, score_y))
    
    pygame.draw.rect(screen, ((255, 255, 255)), score_rect)
    screen.blit(score_surface, score_rect)
    pygame.draw.rect(screen, (0, 0, 0), score_rect, 1)

def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    font = pygame.font.Font(pygame.font.get_default_font(), 36)

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = font.render("3", False, (255, 255, 255))
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = font.render("2", False, (255, 255, 255))
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = font.render("1", False, (255, 255, 255))
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 *  random.choice((1, -1))
        score_time = None


    

def add_point(user):
    global player_points, opponent_points
    if user == 'player':
        player_points += 1
    elif user == 'opponent':
        opponent_points += 1

# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30,30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Game variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

# Text Variables
player_points = 0
opponent_points = 0

# Score Timer
score_time = True

# Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

while True:

    # Handling input
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7

            if event.key == pygame.K_UP:
                player_speed -= 7
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7


    ball_animation()
    player_animation()
    opponent_ai()
    player.y += player_speed
    

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    draw_score()

    if score_time:
        ball_restart()

    # Updating the window
    pygame.display.flip()
    clock.tick(60)