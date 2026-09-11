#!/usr/bin/env python3
"""Star Skirmish — original colourful space shooter (not a licensed title)."""

from __future__ import annotations

import random
import pygame

W, H = 860, 640


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Star Skirmish — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 44, bold=True)

    def reset():
        ship = pygame.Rect(W // 2 - 16, H - 70, 32, 28)
        bullets = []
        foes = [pygame.Rect(60 + i * 70, 80 + (i % 3) * 40, 36, 24) for i in range(10)]
        stars = [(random.randint(0, W), random.randint(0, H), random.randint(1, 3)) for _ in range(70)]
        return ship, bullets, foes, stars, 1, 0, 3, True

    ship, bullets, foes, stars, fdir, score, lives, alive = reset()
    cooldown = 0

    running = True
    while running:
        clock.tick(60)
        cooldown = max(0, cooldown - 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    ship, bullets, foes, stars, fdir, score, lives, alive = reset()

        keys = pygame.key.get_pressed()
        if alive:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ship.x -= 7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ship.x += 7
            ship.x = max(10, min(W - ship.w - 10, ship.x))
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and cooldown == 0:
                bullets.append(pygame.Rect(ship.centerx - 3, ship.y - 12, 6, 14))
                cooldown = 12

            for b in bullets[:]:
                b.y -= 10
                if b.bottom < 0:
                    bullets.remove(b)

            if foes:
                shift = False
                for f in foes:
                    f.x += fdir * 2
                    if f.left < 20 or f.right > W - 20:
                        shift = True
                if shift:
                    fdir *= -1
                    for f in foes:
                        f.y += 16
                for f in foes[:]:
                    for b in bullets[:]:
                        if f.colliderect(b):
                            foes.remove(f)
                            bullets.remove(b)
                            score += 25
                            break
                    if f.colliderect(ship) or f.bottom >= H - 20:
                        lives -= 1
                        foes.remove(f)
                        if lives <= 0:
                            alive = False
                if not foes:
                    foes = [pygame.Rect(60 + i * 70, 60 + (i % 4) * 36, 36, 24) for i in range(12)]
                    fdir = 1

        screen.fill((6, 8, 22))
        for i, (sx, sy, sz) in enumerate(stars):
            sy = (sy + sz) % H
            stars[i] = (sx, sy, sz)
            pygame.draw.circle(screen, (180, 200, 255), (sx, sy), sz)
        pygame.draw.polygon(screen, (80, 230, 255), [
            (ship.centerx, ship.y),
            (ship.left, ship.bottom),
            (ship.centerx, ship.bottom - 8),
            (ship.right, ship.bottom),
        ])
        pygame.draw.polygon(screen, (255, 90, 160), [
            (ship.centerx - 6, ship.bottom),
            (ship.centerx, ship.bottom + 10),
            (ship.centerx + 6, ship.bottom),
        ])
        for b in bullets:
            pygame.draw.rect(screen, (255, 230, 80), b, border_radius=2)
        for f in foes:
            pygame.draw.rect(screen, (255, 70, 110), f, border_radius=4)
            pygame.draw.rect(screen, (255, 200, 80), (f.x + 8, f.y + 6, 20, 8), border_radius=2)

        screen.blit(font.render(f"STAR SKIRMISH   SCORE {score}   LIVES {lives}", True, (255, 220, 90)), (16, 12))
        screen.blit(font.render("← → move   SPACE fire   R restart   ESC menu", True, (160, 170, 210)), (16, H - 28))
        if not alive:
            msg = big.render("SHIP DOWN — press R", True, (255, 80, 120))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
