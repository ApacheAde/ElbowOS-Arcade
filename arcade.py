#!/usr/bin/env python3
"""ElbowOS Arcade — colourful Python 3 mini-games launcher."""

from __future__ import annotations

import importlib
import os
import sys

import pygame

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

GAMES = [
    ("Plumber Jump", "Colourful side-scrolling platformer", "games.plumber_jump"),
    ("Star Skirmish", "Original space shooter", "games.star_skirmish"),
    ("Neon Snake", "Grow, eat, don't crash", "games.neon_snake"),
    ("Brick Bash", "Bat, ball, neon bricks", "games.brick_bash"),
    ("Connect Four", "Drop discs, beat the bot", "games.connect_four"),
    ("Neon Blackjack", "Beat the dealer to 21", "games.blackjack"),
    ("Roulette Royale", "Spin red, black or a number", "games.roulette"),
    ("Lucky Slots", "Three-reel neon slot machine", "games.slots"),
    ("Five-Card Draw", "Poker against the house", "games.poker"),
    ("Neon Craps", "Dice table, play-money bets", "games.craps"),
    ("High-Low", "Guess the next card", "games.high_low"),
    ("Colour Memory", "Match pairs of vivid cards", "games.memory"),
]

W, H = 960, 720
BG = (12, 10, 28)
GOLD = (255, 214, 80)
PINK = (255, 90, 160)
CYAN = (80, 230, 255)
WHITE = (245, 245, 255)
DIM = (90, 90, 120)


def run_game(module_name: str) -> None:
    pygame.quit()
    mod = importlib.import_module(module_name)
    if hasattr(mod, "main"):
        mod.main()
    pygame.init()


def main() -> None:
    pygame.init()
    pygame.display.set_caption("ElbowOS Arcade")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    item_font = pygame.font.SysFont("arial", 24, bold=True)
    hint_font = pygame.font.SysFont("arial", 16)
    selected = 0

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(GAMES)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(GAMES)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    run_game(GAMES[selected][2])
                    pygame.display.set_caption("ElbowOS Arcade")
                    screen = pygame.display.set_mode((W, H))
                    title_font = pygame.font.SysFont("arial", 48, bold=True)
                    item_font = pygame.font.SysFont("arial", 24, bold=True)
                    hint_font = pygame.font.SysFont("arial", 16)

        screen.fill(BG)
        for i in range(18):
            shade = 18 + (i * 4) % 40
            pygame.draw.circle(screen, (shade, 12, 40 + i), (80 + i * 50, 40 + (i * 37) % H), 70, 1)

        title = title_font.render("ELBOWOS ARCADE", True, GOLD)
        screen.blit(title, title.get_rect(center=(W // 2, 52)))
        sub = hint_font.render("Full-colour Python 3 games  •  https://x.com/ElbowOS", True, CYAN)
        screen.blit(sub, sub.get_rect(center=(W // 2, 96)))

        for i, (name, desc, _) in enumerate(GAMES):
            y = 128 + i * 44
            rect = pygame.Rect(140, y - 6, 680, 40)
            if i == selected:
                pygame.draw.rect(screen, PINK, rect, border_radius=10)
                pygame.draw.rect(screen, GOLD, rect, 3, border_radius=10)
                name_c, desc_c = BG, WHITE
            else:
                pygame.draw.rect(screen, (28, 24, 52), rect, border_radius=10)
                pygame.draw.rect(screen, DIM, rect, 2, border_radius=10)
                name_c, desc_c = WHITE, DIM
            screen.blit(item_font.render(name, True, name_c), (160, y))
            screen.blit(hint_font.render(desc, True, desc_c), (420, y + 8))

        hint = hint_font.render("↑↓ select   ENTER play   ESC quit", True, DIM)
        screen.blit(hint, hint.get_rect(center=(W // 2, H - 28)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
