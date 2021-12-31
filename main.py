import pygame, sys
from pygame.locals import *
import random
from enum import Enum


class GameState(Enum):
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
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Game Variables
gravity = 0.13
bird_movement = 0
game_state = GameState.ACTIVE

bg_surface = pygame.image.load("C:/Users/adith/Downloads/background-day.png").convert()
floor_surface = pygame.image.load("C:/Users/adith/Downloads/base.png").convert()
floor_x_pos = 0
floor_surface2 = pygame.image.load("C:/Users/adith/Downloads/base.png").convert()
floor2_x_pos = 288
bird_midflap = pygame.image.load("C:/Users/adith/Downloads/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("C:/Users/adith/AppData/Local/Temp/bluebird-upflap.png").convert_alpha()
bird_downflap = pygame.image.load("C:/Users/adith/Downloads/bluebird-downflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("C:/Users/adith/Downloads/pipe-green.png")
flip_bird = pygame.transform.flip(bird_midflap, False, True)
pipe_list = []
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


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == GameState.ACTIVE:
                if event.key == pygame.K_SPACE or pygame.K_UP:
                    bird_movement = 0
                    bird_movement -= 3.5
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
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        pipe_list = move_pipes(pipe_list)
        move_floor()
        if not check_collision(pipe_list):
            game_state = GameState.CRASH

    if game_state == GameState.CRASH:
        gravity = 0.06
        screen.blit(flip_bird, bird_rect)
        if bird_rect.centery >= 430:
            game_state = GameState.END

    if game_state == GameState.END:
        bird_movement = 0
        gravity = 0
        screen.blit(flip_bird, bird_rect)

    draw_floor()
    draw_pipes(pipe_list)

    pygame.display.update()
    clock.tick(120)
