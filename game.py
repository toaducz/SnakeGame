import streamlit as st
import pygame
import random
import sys

# Cài đặt màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

snake_block = 20
snake_speed = 8
level = 1
count = 0

pygame.init()
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 50)

def our_snake(snake_block, snake_list, screen):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])


def message(msg, color, screen, width, height):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])


def gameLoop():
    global snake_speed, level, count

    WIDTH = 800
    HEIGHT = 600
    screen = pygame.Surface((WIDTH, HEIGHT))

    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 2

    foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, screen)
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            snake_speed += 1
            level += 1

        clock.tick(snake_speed)
        st.image(pygame.surfarray.array3d(screen).swapaxes(0, 1), channels="RGB")

    pygame.quit()
    sys.exit()

if st.button("Start Game"):
    gameLoop()
