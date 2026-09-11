#!/usr/bin/env python3
"""Neon Snake — classic grid snake in full colour."""

from __future__ import annotations

import random
import pygame

W, H = 840, 640
TILE = 20
COLS, ROWS = 40, 28
OX, OY = 20, 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Snake — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    def reset():
        snake = [(8, 8), (7, 8), (6, 8)]
        direction = (1, 0)
        pending = (1, 0)
        apple = (20, 12)
        score = 0
        alive = True
        return snake, direction, pending, apple, score, alive

    snake, direction, pending, apple, score, alive = reset()
    tick = 0
    speed = 8

    running = True
    while running:
        clock.tick(60)
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    snake, direction, pending, apple, score, alive = reset()
                    speed = 8
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    pending = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    pending = (1, 0)
                elif event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    pending = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    pending = (0, 1)

        if alive and tick % max(3, 14 - speed) == 0:
            direction = pending
            hx, hy = snake[0]
            nx, ny = hx + direction[0], hy + direction[1]
            if nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS or (nx, ny) in snake:
                alive = False
            else:
                snake.insert(0, (nx, ny))
                if (nx, ny) == apple:
                    score += 10
                    speed = min(12, 8 + score // 50)
                    while True:
                        apple = (random.randrange(COLS), random.randrange(ROWS))
                        if apple not in snake:
                            break
                else:
                    snake.pop()

        screen.fill((8, 12, 24))
        pygame.draw.rect(screen, (20, 40, 70), (OX - 4, OY - 4, COLS * TILE + 8, ROWS * TILE + 8), 3, border_radius=6)
        for i, (x, y) in enumerate(snake):
            t = i / max(1, len(snake))
            col = (int(40 + 200 * (1 - t)), int(255 * (1 - t * 0.4)), int(180 + 70 * t))
            pygame.draw.rect(screen, col, (OX + x * TILE + 1, OY + y * TILE + 1, TILE - 2, TILE - 2), border_radius=4)
        pygame.draw.circle(screen, (255, 80, 120), (OX + apple[0] * TILE + TILE // 2, OY + apple[1] * TILE + TILE // 2), 8)
        screen.blit(font.render(f"NEON SNAKE   SCORE {score}   length {len(snake)}", True, (80, 255, 210)), (20, 16))
        screen.blit(font.render("WASD / arrows  R restart  ESC menu", True, (160, 170, 200)), (20, H - 28))
        if not alive:
            msg = big.render("CRASH — press R", True, (255, 70, 110))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
