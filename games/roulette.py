#!/usr/bin/env python3
"""Roulette Royale — colourful European roulette."""

from __future__ import annotations

import math
import random
import pygame

W, H = 960, 640
RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ORDER = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
         5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]


def colour_of(n: int) -> str:
    if n == 0:
        return "green"
    return "red" if n in RED else "black"


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Roulette Royale — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 40, bold=True)
    ui = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 16)
    num_font = pygame.font.SysFont("arial", 14, bold=True)

    bank = 500
    bet_amt = 10
    choice = "red"
    number = 17
    angle = 0.0
    spin_v = 0.0
    spinning = False
    result = None
    message = "Pick red, black or a number, then SPACE to spin"

    cx, cy, radius = 280, 340, 210

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    bet_amt = max(5, bet_amt - 5)
                elif event.key == pygame.K_RIGHT:
                    bet_amt = min(100, bet_amt + 5)
                elif event.key == pygame.K_r:
                    choice = "red"
                elif event.key == pygame.K_b:
                    choice = "black"
                elif event.key == pygame.K_n:
                    choice = "number"
                elif event.key == pygame.K_UP:
                    number = 0 if number == 36 else number + 1
                    choice = "number"
                elif event.key == pygame.K_DOWN:
                    number = 36 if number == 0 else number - 1
                    choice = "number"
                elif event.key == pygame.K_SPACE and not spinning and bank >= bet_amt:
                    bank -= bet_amt
                    spinning = True
                    result = None
                    spin_v = random.uniform(18, 26)
                    message = "No more bets..."

        if spinning:
            angle = (angle + spin_v) % 360
            spin_v *= 0.985
            if spin_v < 0.12:
                spinning = False
                slice_a = 360 / 37
                idx = int(((-angle) % 360) / slice_a) % 37
                result = ORDER[idx]
                col = colour_of(result)
                win = 0
                if choice == col:
                    win = bet_amt * 2
                elif choice == "number" and number == result:
                    win = bet_amt * 36
                if win:
                    bank += win
                    message = f"{result} {col.upper()} — you win £{win}"
                else:
                    message = f"{result} {col.upper()} — house takes the pot"

        screen.fill((18, 12, 28))
        pygame.draw.circle(screen, (40, 20, 10), (cx, cy), radius + 18)
        pygame.draw.circle(screen, (180, 140, 50), (cx, cy), radius + 12, 6)

        slice_a = 360 / 37
        for i, n in enumerate(ORDER):
            start = math.radians(i * slice_a + angle)
            end = math.radians((i + 1) * slice_a + angle)
            col = (20, 130, 55) if n == 0 else ((190, 30, 40) if n in RED else (18, 18, 22))
            pts = [(cx, cy)]
            steps = 6
            for s in range(steps + 1):
                a = start + (end - start) * s / steps
                pts.append((cx + math.cos(a) * radius, cy + math.sin(a) * radius))
            pygame.draw.polygon(screen, col, pts)
            mid = start + (end - start) / 2
            tx = cx + math.cos(mid) * (radius - 28)
            ty = cy + math.sin(mid) * (radius - 28)
            label = num_font.render(str(n), True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(tx, ty)))

        pygame.draw.circle(screen, (210, 170, 60), (cx, cy), 28)
        pygame.draw.polygon(screen, (255, 220, 80), [(cx + radius - 8, cy), (cx + radius + 22, cy - 10), (cx + radius + 22, cy + 10)])

        panel = pygame.Rect(540, 70, 380, 500)
        pygame.draw.rect(screen, (32, 22, 48), panel, border_radius=16)
        pygame.draw.rect(screen, (255, 200, 70), panel, 3, border_radius=16)
        screen.blit(title.render("ROULETTE", True, (255, 210, 70)), (70, 36))
        lines = [
            f"Bank   £{bank}",
            f"Bet    £{bet_amt}",
            f"Wager  {choice.upper()}" + (f"  ({number})" if choice == "number" else ""),
            "",
            message,
            "",
            "R red    B black    N number",
            "↑↓ change number",
            "← → change bet",
            "SPACE spin    ESC menu",
        ]
        for i, line in enumerate(lines):
            screen.blit(ui.render(line, True, (240, 230, 255) if i < 5 else (180, 170, 210)), (560, 100 + i * 34))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
