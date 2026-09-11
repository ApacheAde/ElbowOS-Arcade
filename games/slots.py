#!/usr/bin/env python3
"""Lucky Slots — three-reel neon slot machine."""

from __future__ import annotations

import random
import pygame

W, H = 900, 640
SYMBOLS = [
    ("CHERRY", (220, 40, 70), 4),
    ("LEMON", (250, 210, 50), 5),
    ("BELL", (255, 180, 40), 8),
    ("BAR", (90, 200, 255), 12),
    ("SEVEN", (255, 50, 80), 25),
    ("STAR", (255, 230, 90), 40),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lucky Slots — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 48, bold=True)
    ui = pygame.font.SysFont("arial", 26, bold=True)
    sym_font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 250
    bet = 5
    reels = [0, 1, 2]
    spinning = [False, False, False]
    timers = [0, 0, 0]
    message = "SPACE to spin"

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    bet = max(1, bet - 1)
                elif event.key == pygame.K_RIGHT:
                    bet = min(25, bet + 1)
                elif event.key == pygame.K_SPACE and not any(spinning) and bank >= bet:
                    bank -= bet
                    spinning[:] = [True, True, True]
                    timers[:] = [900, 1300, 1700]
                    message = "Good luck..."

        if any(spinning):
            for i in range(3):
                if spinning[i]:
                    timers[i] -= dt
                    if random.random() < 0.45:
                        reels[i] = (reels[i] + 1) % len(SYMBOLS)
                    if timers[i] <= 0:
                        spinning[i] = False
                        reels[i] = random.randrange(len(SYMBOLS))
            if not any(spinning):
                a, b, c = reels
                if a == b == c:
                    payout = bet * SYMBOLS[a][2]
                    bank += payout
                    message = f"JACKPOT {SYMBOLS[a][0]}  +£{payout}"
                elif a == b or b == c or a == c:
                    payout = bet * 2
                    bank += payout
                    message = f"Pair pays  +£{payout}"
                else:
                    message = "No luck — spin again"

        screen.fill((16, 8, 28))
        pygame.draw.rect(screen, (90, 20, 40), (40, 30, W - 80, H - 60), border_radius=20)
        pygame.draw.rect(screen, (255, 200, 70), (40, 30, W - 80, H - 60), 5, border_radius=20)
        head = title.render("LUCKY SLOTS", True, (255, 220, 80))
        screen.blit(head, head.get_rect(center=(W // 2, 80)))

        for i, idx in enumerate(reels):
            name, col, _ = SYMBOLS[idx]
            box = pygame.Rect(120 + i * 230, 160, 200, 240)
            pygame.draw.rect(screen, (10, 10, 18), box, border_radius=16)
            pygame.draw.rect(screen, col, box, 6, border_radius=16)
            pygame.draw.circle(screen, col, box.center, 54)
            pygame.draw.circle(screen, (20, 12, 24), box.center, 40)
            label = sym_font.render(name, True, col)
            screen.blit(label, label.get_rect(center=(box.centerx, box.bottom - 28)))

        screen.blit(ui.render(f"Bank  £{bank}", True, (255, 255, 255)), (80, 440))
        screen.blit(ui.render(f"Bet  £{bet}", True, (255, 210, 80)), (320, 440))
        msg = ui.render(message, True, (120, 255, 200))
        screen.blit(msg, (80, 490))
        screen.blit(small.render("← → change bet   SPACE spin   ESC menu", True, (200, 180, 210)), (80, 560))
        pay = "Pays: pair x2   triple cherry x4  lemon x5  bell x8  bar x12  seven x25  star x40"
        screen.blit(small.render(pay, True, (180, 160, 190)), (80, 590))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
