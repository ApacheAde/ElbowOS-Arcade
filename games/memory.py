#!/usr/bin/env python3
"""Colour Memory — match vivid pairs."""

from __future__ import annotations

import random
import time

import pygame

W, H = 900, 640
COLS, ROWS = 4, 3
PAD_X, PAD_Y = 40, 120
CARD_W, CARD_H = 180, 140
GAP = 20

PAIRS = [
    ("RUBY", (220, 40, 70)),
    ("SUN", (255, 200, 40)),
    ("LIME", (90, 210, 70)),
    ("AZURE", (50, 160, 255)),
    ("VIOLET", (160, 80, 255)),
    ("CORAL", (255, 110, 80)),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Colour Memory — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 40, bold=True)
    ui = pygame.font.SysFont("arial", 22, bold=True)
    name_font = pygame.font.SysFont("arial", 22, bold=True)

    def new_board():
        items = PAIRS * 2
        random.shuffle(items)
        return items

    board = new_board()
    revealed = [False] * (COLS * ROWS)
    matched = [False] * (COLS * ROWS)
    pick: list[int] = []
    freeze_until = 0.0
    moves = 0
    won = False
    started = time.time()

    running = True
    while running:
        clock.tick(60)
        now = time.time()
        if freeze_until and now >= freeze_until:
            if board[pick[0]][0] != board[pick[1]][0]:
                revealed[pick[0]] = revealed[pick[1]] = False
            else:
                matched[pick[0]] = matched[pick[1]] = True
            pick = []
            freeze_until = 0.0
            if all(matched):
                won = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    board = new_board()
                    revealed = [False] * 12
                    matched = [False] * 12
                    pick = []
                    freeze_until = 0.0
                    moves = 0
                    won = False
                    started = time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN and not won and not freeze_until:
                mx, my = event.pos
                for i in range(12):
                    c, r = i % COLS, i // COLS
                    rect = pygame.Rect(PAD_X + c * (CARD_W + GAP), PAD_Y + r * (CARD_H + GAP), CARD_W, CARD_H)
                    if rect.collidepoint(mx, my) and not revealed[i] and not matched[i]:
                        revealed[i] = True
                        pick.append(i)
                        if len(pick) == 2:
                            moves += 1
                            freeze_until = now + 0.7

        screen.fill((16, 18, 40))
        screen.blit(title.render("COLOUR MEMORY", True, (255, 220, 80)), (40, 28))
        elapsed = int(now - started)
        screen.blit(ui.render(f"Moves {moves}    Time {elapsed}s    R restart", True, (200, 210, 255)), (40, 76))

        for i in range(12):
            c, r = i % COLS, i // COLS
            rect = pygame.Rect(PAD_X + c * (CARD_W + GAP), PAD_Y + r * (CARD_H + GAP), CARD_W, CARD_H)
            if revealed[i] or matched[i]:
                name, col = board[i]
                pygame.draw.rect(screen, col, rect, border_radius=14)
                pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=14)
                label = name_font.render(name, True, (20, 16, 28))
                screen.blit(label, label.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, (50, 60, 140), rect, border_radius=14)
                pygame.draw.rect(screen, (255, 200, 70), rect, 3, border_radius=14)
                pygame.draw.circle(screen, (255, 90, 160), rect.center, 18, 4)

        if won:
            banner = title.render(f"CLEARED in {moves} moves!", True, (255, 230, 80))
            screen.blit(banner, banner.get_rect(center=(W // 2, H - 36)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
