import pygame, sys
from pygame.locals import *
import random
from enum import Enum


class GameState(Enum):
    NOTSTARTED = 0
    ACTIVE = 1
    CRASH = 2
    END = 3


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 450:
        return False

    return True


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(score):
    if game_state == GameState.NOTSTARTED:
        return
    elif game_state == GameState.END:
        score_surface = final_score_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 256))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)


def calculate_score(pipes, score):
    for pipe in pipes:
        if pipe.centerx - 1 <= bird_rect.centerx <= pipe.centerx + 1:
            score += 0.5

    return score


pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
game_font = pygame.font.Font('./assets/04B_19.TTF', 20)
final_score_font = pygame.font.Font('./assets/04B_19.TTF', 50)

# Game Variables
bg_surface = pygame.image.load("./assets/background-day.png").convert()
floor_surface = pygame.image.load("./assets/base.png").convert()
floor_surface2 = pygame.image.load("./assets/base.png").convert()
bird_midflap = pygame.image.load("./assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("./assets/bluebird-upflap.png").convert_alpha()
bird_downflap = pygame.image.load("./assets/bluebird-downflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
gravity = 0
bird_movement = 0
game_state = GameState.NOTSTARTED
score = 0
high_score = 0
floor_x_pos = 0
floor2_x_pos = 288
bird_index = 0

bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("./assets/pipe-green.png")
flip_bird = pygame.transform.flip(bird_midflap, False, True)

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]


def move_floor():
    global floor_x_pos, floor2_x_pos
    floor2_x_pos -= 1
    floor_x_pos -= 1
    if floor_x_pos <= -288:
        floor_x_pos = 288
    if floor2_x_pos <= -288:
        floor2_x_pos = 288


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface2, (floor2_x_pos, 450))


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 4.5, 1)
    return new_bird


def new_game():

    global bird_movement, bird_index, bird_surface, bird_rect, score, game_state, gravity
    bird_movement = 0
    game_state = GameState.NOTSTARTED
    score = 0
    high_score = 0
    bird_index = 0
    bird_rect = bird_surface.get_rect(center=(50, 256))
    floor_x_pos = 0
    floor2_x_pos = 288
    gravity = 0
    pipe_list = []
    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_state == GameState.NOTSTARTED and event.key == pygame.K_s:
                    game_state = GameState.ACTIVE
                if game_state == GameState.END and event.key == pygame.K_r:
                    return
                if game_state == GameState.ACTIVE:
                    if event.key == pygame.K_SPACE or pygame.K_UP:
                        bird_movement = 0
                        bird_movement -= 3.5
            if game_state != GameState.NOTSTARTED:
                if event.type == SPAWNPIPE:
                    pipe_list.extend(create_pipe())
            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface, bird_rect = bird_animation()

        screen.blit(bg_surface, (0, 0))
        bird_movement += gravity
        bird_rect.centery += bird_movement
        if game_state == GameState.ACTIVE:
            gravity = 0.13
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            pipe_list = move_pipes(pipe_list)
            move_floor()
            draw_pipes(pipe_list)
            score = calculate_score(pipe_list, score)
            if not check_collision(pipe_list):
                game_state = GameState.CRASH

        if game_state == GameState.CRASH:
            draw_pipes(pipe_list)
            gravity = 0.06
            screen.blit(flip_bird, bird_rect)
            if bird_rect.centery >= 436:
                game_state = GameState.END
                pygame.time.delay(1000)


        if game_state == GameState.END:
            bird_movement = 0
            gravity = 0
            end_game_surface = game_font.render("Press R to Restart", True, (255, 255, 255))
            end_game_rect = end_game_surface.get_rect(center=(144, 50))
            screen.blit(end_game_surface, end_game_rect)
            game_over_surface = final_score_font.render("GAME OVER!", True, (255, 0, 0))
            game_over_rect = game_over_surface.get_rect(center=(144, 350))
            screen.blit(game_over_surface, game_over_rect)
        if game_state == GameState.NOTSTARTED:
            gravity = 0
            screen.blit(bird_surface, bird_rect)
            start_game_surface = game_font.render("Press S to Start", True, (255, 255, 255))
            start_game_rect = start_game_surface.get_rect(center=(144, 50))
            screen.blit(start_game_surface, start_game_rect)

        draw_floor()
        score_display(score)
        pygame.display.update()
        clock.tick(120)

while True:
    new_game()
