#!/usr/bin/env python3
"""Brick Bash — colourful breakout-style bat and ball."""

from __future__ import annotations

import pygame

W, H = 860, 640


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Brick Bash — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 44, bold=True)

    def reset():
        paddle = pygame.Rect(W // 2 - 60, H - 40, 120, 16)
        ball = pygame.Rect(W // 2 - 8, H - 70, 16, 16)
        vx, vy = 4.2, -4.8
        colors = [(255, 80, 120), (255, 160, 60), (255, 220, 70), (80, 220, 140), (70, 180, 255)]
        bricks = []
        for row in range(5):
            for col in range(10):
                bricks.append((pygame.Rect(40 + col * 78, 70 + row * 32, 72, 24), colors[row]))
        return paddle, ball, vx, vy, bricks, 0, 3, False

    paddle, ball, vx, vy, bricks, score, lives, started = reset()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    paddle, ball, vx, vy, bricks, score, lives, started = reset()
                elif event.key == pygame.K_SPACE:
                    started = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle.x -= 8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle.x += 8
        paddle.x = max(10, min(W - paddle.w - 10, paddle.x))

        if started and lives > 0 and bricks:
            ball.x += int(vx)
            ball.y += int(vy)
            if ball.left <= 10 or ball.right >= W - 10:
                vx *= -1
            if ball.top <= 50:
                vy *= -1
            if ball.colliderect(paddle) and vy > 0:
                vy *= -1
                offset = (ball.centerx - paddle.centerx) / (paddle.w / 2)
                vx = max(-7, min(7, vx + offset * 2.2))
            for brick, col in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove((brick, col))
                    vy *= -1
                    score += 10
                    break
            if ball.top > H:
                lives -= 1
                ball.topleft = (paddle.centerx - 8, H - 70)
                vx, vy = 4.2, -4.8
                started = False

        screen.fill((14, 10, 28))
        pygame.draw.rect(screen, (40, 30, 70), (8, 48, W - 16, H - 56), 2, border_radius=8)
        for brick, col in bricks:
            pygame.draw.rect(screen, col, brick, border_radius=4)
            pygame.draw.rect(screen, (255, 255, 255), brick, 1, border_radius=4)
        pygame.draw.rect(screen, (255, 90, 180), paddle, border_radius=8)
        pygame.draw.circle(screen, (255, 240, 120), ball.center, 8)
        screen.blit(font.render(f"BRICK BASH   SCORE {score}   LIVES {lives}", True, (255, 220, 90)), (16, 12))
        screen.blit(font.render("← → move   SPACE launch   R restart   ESC menu", True, (180, 180, 210)), (16, H - 24))
        if not bricks:
            msg = big.render("ALL CLEAR!", True, (80, 255, 160))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        elif lives <= 0:
            msg = big.render("NO LIVES — press R", True, (255, 80, 120))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        elif not started:
            msg = font.render("SPACE to serve", True, (255, 255, 255))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
