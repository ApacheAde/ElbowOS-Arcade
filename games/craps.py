#!/usr/bin/env python3
"""Neon Craps — colourful casino dice table (play money)."""

from __future__ import annotations

import random
import pygame

W, H = 900, 620
GREEN = (18, 92, 52)
GOLD = (255, 214, 80)
WHITE = (250, 250, 255)
PINK = (255, 90, 160)


def roll():
    return random.randint(1, 6), random.randint(1, 6)


def draw_die(surf, x, y, n, col):
    pygame.draw.rect(surf, col, (x, y, 72, 72), border_radius=12)
    pygame.draw.rect(surf, (30, 30, 40), (x, y, 72, 72), 3, border_radius=12)
    spots = {
        1: [(36, 36)],
        2: [(20, 20), (52, 52)],
        3: [(20, 20), (36, 36), (52, 52)],
        4: [(20, 20), (52, 20), (20, 52), (52, 52)],
        5: [(20, 20), (52, 20), (36, 36), (20, 52), (52, 52)],
        6: [(20, 20), (52, 20), (20, 36), (52, 36), (20, 52), (52, 52)],
    }
    for sx, sy in spots[n]:
        pygame.draw.circle(surf, (20, 20, 30), (x + sx, y + sy), 6)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Craps — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 42, bold=True)

    bank = 500
    bet = 25
    point = None
    dice = (1, 1)
    msg = "Come-out roll. SPACE to throw. 7 or 11 win, 2/3/12 lose."
    anim = 0

    running = True
    while running:
        clock.tick(60)
        if anim:
            anim -= 1
            if anim:
                dice = roll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    bet = max(5, bet - 5)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    bet = min(bank, bet + 5)
                elif event.key == pygame.K_r:
                    bank, bet, point, msg = 500, 25, None, "Fresh bankroll. SPACE to throw."
                elif event.key == pygame.K_SPACE and anim == 0 and bank >= bet:
                    anim = 18

        if anim == 1:
            a, b = dice
            total = a + b
            if point is None:
                if total in (7, 11):
                    bank += bet
                    msg = f"Natural {total}! You win ${bet}."
                elif total in (2, 3, 12):
                    bank -= bet
                    msg = f"Craps {total}. You lose ${bet}."
                else:
                    point = total
                    msg = f"Point is {point}. Hit it before 7."
            else:
                if total == point:
                    bank += bet
                    msg = f"Hit the point {point}! You win ${bet}."
                    point = None
                elif total == 7:
                    bank -= bet
                    msg = "Seven-out. You lose."
                    point = None
                else:
                    msg = f"Rolled {total}. Point still {point}."
            bet = min(bet, max(5, bank))
            if bank <= 0:
                msg = "Busted. Press R for a new bankroll."

        screen.fill((8, 28, 18))
        pygame.draw.rect(screen, GREEN, (30, 80, W - 60, H - 140), border_radius=24)
        pygame.draw.rect(screen, GOLD, (30, 80, W - 60, H - 140), 6, border_radius=24)
        screen.blit(big.render("NEON CRAPS", True, GOLD), (40, 20))
        screen.blit(font.render("Play-money only  •  https://x.com/ElbowOS", True, WHITE), (420, 36))

        draw_die(screen, 320, 220, dice[0], (250, 245, 235))
        draw_die(screen, 420, 220, dice[1], (250, 245, 235))
        screen.blit(big.render(str(sum(dice)), True, WHITE), (530, 230))

        screen.blit(font.render(f"BANK  ${bank}", True, GOLD), (60, 120))
        screen.blit(font.render(f"BET   ${bet}   ← → change", True, WHITE), (60, 156))
        screen.blit(font.render(f"POINT {point if point else 'come-out'}", True, PINK), (60, 192))
        screen.blit(font.render(msg, True, WHITE), (60, 360))
        screen.blit(font.render("SPACE throw   R reset bank   ESC menu", True, (200, 220, 180)), (60, H - 40))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
