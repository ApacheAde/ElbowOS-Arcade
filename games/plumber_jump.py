#!/usr/bin/env python3
"""Plumber Jump — original colourful platformer (not an emulator)."""

from __future__ import annotations

import random
import pygame

W, H = 960, 540
GRAVITY = 0.55
JUMP = -12.5
SPEED = 5.2


class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.w, self.h = 34, 42
        self.on_ground = False
        self.facing = 1
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, platforms):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False

        self.vy += GRAVITY
        self.x += self.vx
        r = self.rect
        for p in platforms:
            if r.colliderect(p):
                if self.vx > 0:
                    self.x = p.left - self.w
                elif self.vx < 0:
                    self.x = p.right
                r = self.rect

        self.y += self.vy
        r = self.rect
        self.on_ground = False
        for p in platforms:
            if r.colliderect(p):
                if self.vy > 0:
                    self.y = p.top - self.h
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.bottom
                    self.vy = 0
                r = self.rect

    def draw(self, surf, cam):
        x = int(self.x - cam)
        body = pygame.Rect(x + 6, int(self.y) + 14, 22, 24)
        pygame.draw.rect(surf, (230, 50, 70), body, border_radius=4)
        pygame.draw.rect(surf, (40, 90, 220), (x + 8, int(self.y) + 28, 18, 14), border_radius=3)
        pygame.draw.circle(surf, (255, 210, 160), (x + 17, int(self.y) + 12), 10)
        pygame.draw.rect(surf, (230, 50, 70), (x + 6, int(self.y) + 2, 22, 8), border_radius=3)
        eye = x + 20 if self.facing > 0 else x + 10
        pygame.draw.circle(surf, (20, 20, 30), (eye, int(self.y) + 12), 2)


class Enemy:
    def __init__(self, x, y, left, right):
        self.x, self.y = x, y
        self.left, self.right = left, right
        self.dir = 1
        self.w, self.h = 32, 28

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.x += self.dir * 1.6
        if self.x < self.left or self.x > self.right:
            self.dir *= -1

    def draw(self, surf, cam):
        x = int(self.x - cam)
        pygame.draw.ellipse(surf, (160, 70, 30), (x, int(self.y), self.w, self.h))
        pygame.draw.ellipse(surf, (90, 40, 16), (x + 4, int(self.y) + 6, 10, 8))
        pygame.draw.ellipse(surf, (90, 40, 16), (x + 18, int(self.y) + 6, 10, 8))


def make_level():
    ground = []
    coins = []
    pieces = [(0, 492, 720, 48), (860, 492, 520, 48), (1500, 492, 900, 48),
              (2520, 492, 700, 48), (3400, 492, 900, 48)]
    for x, y, w, h in pieces:
        ground.append(pygame.Rect(x, y, w, h))
    platforms = [
        (220, 400, 160, 20), (480, 330, 140, 20), (760, 280, 120, 20),
        (1080, 380, 160, 20), (1280, 300, 140, 20), (1700, 400, 180, 20),
        (1960, 320, 140, 20), (2180, 250, 160, 20), (2700, 380, 180, 20),
        (3000, 300, 140, 20), (3600, 400, 160, 20), (3850, 320, 180, 20),
    ]
    for x, y, w, h in platforms:
        ground.append(pygame.Rect(x, y, w, h))
        coins.append(pygame.Rect(x + w // 2 - 8, y - 28, 16, 16))
    enemies = [
        Enemy(260, 464, 40, 680),
        Enemy(980, 464, 860, 1320),
        Enemy(1760, 464, 1520, 2300),
        Enemy(2740, 464, 2520, 3160),
        Enemy(1740, 372, 1700, 1860),
    ]
    flag = pygame.Rect(4180, 360, 18, 132)
    return ground, enemies, coins, flag


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Plumber Jump — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    platforms, enemies, coins, flag = make_level()
    player = Player(60, 400)
    cam = 0
    score = 0
    won = False
    dead = False
    clouds = [(random.randint(0, 4500), random.randint(40, 180), random.randint(50, 110)) for _ in range(18)]

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                platforms, enemies, coins, flag = make_level()
                player = Player(60, 400)
                cam = score = 0
                won = dead = False

        keys = pygame.key.get_pressed()
        if player.alive and not won:
            player.update(keys, platforms)
            for e in list(enemies):
                e.update()
                if player.rect.colliderect(e.rect):
                    if player.vy > 2 and player.rect.bottom - e.rect.top < 18:
                        enemies.remove(e)
                        player.vy = JUMP * 0.55
                        score += 150
                    else:
                        player.alive = False
                        dead = True
            for c in coins[:]:
                if player.rect.colliderect(c):
                    coins.remove(c)
                    score += 50
            if player.rect.colliderect(flag):
                won = True
            if player.y > H + 80:
                player.alive = False
                dead = True

        cam = max(0, int(player.x) - 280)

        screen.fill((92, 180, 255))
        pygame.draw.rect(screen, (70, 160, 245), (0, 0, W, 220))
        for cx, cy, cw in clouds:
            pygame.draw.ellipse(screen, (255, 255, 255), (cx - cam * 0.4, cy, cw, 28))
            pygame.draw.ellipse(screen, (255, 255, 255), (cx - cam * 0.4 + 20, cy - 10, cw * 0.7, 30))

        for hx in range(-100, 5000, 280):
            pygame.draw.ellipse(screen, (50, 170, 80), (hx - cam * 0.6, 390, 340, 160))

        for p in platforms:
            r = pygame.Rect(p.x - cam, p.y, p.w, p.h)
            pygame.draw.rect(screen, (210, 120, 50), r)
            pygame.draw.rect(screen, (70, 180, 70), (r.x, r.y, r.w, 8))
            pygame.draw.rect(screen, (150, 80, 30), r, 2)

        for c in coins:
            pygame.draw.circle(screen, (255, 210, 40), (c.x - cam + 8, c.y + 8), 8)
            pygame.draw.circle(screen, (255, 240, 140), (c.x - cam + 8, c.y + 8), 4)

        for e in enemies:
            e.draw(screen, cam)

        pygame.draw.rect(screen, (40, 40, 50), (flag.x - cam, flag.y, 8, flag.h))
        pygame.draw.polygon(screen, (40, 200, 90), [
            (flag.x - cam + 8, flag.y),
            (flag.x - cam + 70, flag.y + 22),
            (flag.x - cam + 8, flag.y + 44),
        ])

        player.draw(screen, cam)
        screen.blit(font.render(f"SCORE  {score}", True, (20, 30, 50)), (16, 12))
        screen.blit(font.render("ARROWS/WASD move  SPACE jump  R restart  ESC menu", True, (20, 30, 50)), (16, H - 28))

        if won:
            msg = big.render("LEVEL CLEAR!", True, (255, 230, 60))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        elif dead:
            msg = big.render("OUCH — press R", True, (255, 60, 80))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
