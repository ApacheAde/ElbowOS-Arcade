#!/usr/bin/env python3
"""High-Low — colourful card guessing game."""

from __future__ import annotations

import random
import pygame

W, H = 860, 600
SUITS = "♠♥♦♣"
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RED = (220, 50, 70)
BLACK = (25, 25, 35)
GOLD = (255, 214, 80)


def value(card):
    return RANKS.index(card[0])


def draw_card(surf, x, y, card, font, small):
    rank, suit = card
    pygame.draw.rect(surf, (250, 248, 240), (x, y, 140, 200), border_radius=12)
    pygame.draw.rect(surf, (30, 30, 40), (x, y, 140, 200), 3, border_radius=12)
    col = RED if suit in "♥♦" else BLACK
    surf.blit(font.render(rank, True, col), (x + 12, y + 10))
    surf.blit(small.render(suit, True, col), (x + 14, y + 48))
    bigs = pygame.font.SysFont("arial", 64, bold=True)
    glyph = bigs.render(suit, True, col)
    surf.blit(glyph, glyph.get_rect(center=(x + 70, y + 120)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("High-Low — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28, bold=True)
    small = pygame.font.SysFont("arial", 24, bold=True)
    hint = pygame.font.SysFont("arial", 20, bold=True)

    def new_card():
        return random.choice(RANKS), random.choice(SUITS)

    bank = 300
    bet = 20
    current = new_card()
    nextc = None
    streak = 0
    guess = "H"
    msg = "Will the next card be HIGHER or LOWER?"
    reveal = 0

    running = True
    while running:
        clock.tick(60)
        if reveal:
            reveal -= 1
            if reveal == 0:
                if nextc is not None:
                    cv, nv = value(current), value(nextc)
                    if nv == cv:
                        msg = "Push — same rank. Bet returned."
                    elif (guess == "H" and nv > cv) or (guess == "L" and nv < cv):
                        bank += bet
                        streak += 1
                        msg = f"Correct! {nextc[0]}{nextc[1]}  +${bet}  streak {streak}"
                    else:
                        bank -= bet
                        streak = 0
                        msg = f"Wrong. {nextc[0]}{nextc[1]}  -${bet}"
                    current = nextc
                    nextc = None
                    bet = min(bet, max(10, bank))
                    if bank <= 0:
                        msg = "Busted. Press R for a new bankroll."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    bank, bet, current, nextc, streak = 300, 20, new_card(), None, 0
                    msg = "Fresh shoe. Higher or lower?"
                    reveal = 0
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    bet = max(10, bet - 10)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    bet = min(max(10, bank), bet + 10)
                elif event.key in (pygame.K_h, pygame.K_UP) and reveal == 0 and bank >= bet:
                    guess = "H"
                    nextc = new_card()
                    reveal = 24
                elif event.key in (pygame.K_l, pygame.K_DOWN) and reveal == 0 and bank >= bet:
                    guess = "L"
                    nextc = new_card()
                    reveal = 24

        screen.fill((28, 16, 48))
        screen.blit(font.render("HIGH  /  LOW", True, GOLD), (40, 24))
        screen.blit(hint.render("Play-money card game  •  https://x.com/ElbowOS", True, (200, 180, 255)), (320, 34))
        screen.blit(hint.render(f"BANK ${bank}    BET ${bet}    STREAK {streak}", True, (255, 255, 255)), (40, 80))

        draw_card(screen, 220, 160, current, font, small)
        if nextc and reveal < 12:
            draw_card(screen, 500, 160, nextc, font, small)
        else:
            pygame.draw.rect(screen, (80, 40, 140), (500, 160, 140, 200), border_radius=12)
            pygame.draw.rect(screen, GOLD, (500, 160, 140, 200), 3, border_radius=12)
            q = font.render("?", True, GOLD)
            screen.blit(q, q.get_rect(center=(570, 260)))

        screen.blit(hint.render(msg, True, (255, 230, 180)), (40, 400))
        screen.blit(hint.render("H / ↑  higher     L / ↓  lower     ← → bet     R reset     ESC menu", True, (180, 170, 210)), (40, H - 36))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
