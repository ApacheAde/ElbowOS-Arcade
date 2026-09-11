#!/usr/bin/env python3
"""Five-Card Draw — colourful poker versus the house."""

from __future__ import annotations

import random
from collections import Counter

import pygame

W, H = 960, 640
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VAL = {r: i for i, r in enumerate(RANKS)}
RED = {"\u2665", "\u2666"}


def deck():
    cards = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(cards)
    return cards


def hand_rank(hand):
    ranks = sorted((RANK_VAL[r] for r, _ in hand), reverse=True)
    suits = [s for _, s in hand]
    counts = Counter(ranks)
    freqs = sorted(counts.values(), reverse=True)
    unique = sorted(counts.keys(), key=lambda r: (counts[r], r), reverse=True)
    flush = len(set(suits)) == 1
    straight = False
    sr = sorted(set(ranks))
    if len(sr) == 5 and sr[-1] - sr[0] == 4:
        straight = True
    if set(ranks) == {12, 0, 1, 2, 3}:
        straight = True
        unique = [3, 2, 1, 0, -1]
    if straight and flush:
        return (8, unique)
    if freqs == [4, 1]:
        return (7, unique)
    if freqs == [3, 2]:
        return (6, unique)
    if flush:
        return (5, ranks)
    if straight:
        return (4, unique)
    if freqs == [3, 1, 1]:
        return (3, unique)
    if freqs == [2, 2, 1]:
        return (2, unique)
    if freqs == [2, 1, 1, 1]:
        return (1, unique)
    return (0, ranks)


NAMES = {
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card",
}


def draw_card(surf, card, x, y, selected=False):
    rect = pygame.Rect(x, y, 100, 144)
    pygame.draw.rect(surf, (250, 248, 240), rect, border_radius=10)
    border = (255, 210, 60) if selected else (30, 30, 40)
    pygame.draw.rect(surf, border, rect, 4 if selected else 2, border_radius=10)
    rank, suit = card
    colour = (200, 30, 50) if suit in RED else (20, 20, 30)
    font = pygame.font.SysFont("arial", 26, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)
    surf.blit(font.render(rank, True, colour), (x + 8, y + 8))
    surf.blit(big.render(suit, True, colour), (x + 30, y + 50))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Five-Card Draw — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 40, bold=True)
    ui = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 400
    bet = 20
    d = []
    player = []
    dealer = []
    hold = [False] * 5
    phase = "ready"
    message = "D to deal — click or 1-5 to hold cards, then DRAW"

    def deal():
        nonlocal d, player, dealer, hold, phase, bank, message
        if bank < bet:
            message = "Need more chips"
            return
        bank -= bet
        d = deck()
        player = [d.pop() for _ in range(5)]
        dealer = [d.pop() for _ in range(5)]
        hold = [False] * 5
        phase = "hold"
        message = "Hold cards (1-5 / click), then ENTER to draw"

    def draw():
        nonlocal phase, bank, message
        for i in range(5):
            if not hold[i]:
                player[i] = d.pop()
        dh = [False] * 5
        rank, _ = hand_rank(dealer)
        if rank == 0:
            dh = [False, False, False, False, True]
        elif rank == 1:
            counts = Counter(r for r, _ in dealer)
            pair_r = max(counts, key=counts.get)
            dh = [RANK_VAL[r] == pair_r for r, _ in dealer]
        for i in range(5):
            if not dh[i]:
                dealer[i] = d.pop()
        pr, dr = hand_rank(player), hand_rank(dealer)
        if pr > dr:
            bank += bet * 2
            message = f"{NAMES[pr[0]]} beats {NAMES[dr[0]]} — you win \u00a3{bet * 2}"
        elif pr == dr:
            bank += bet
            message = "Tie — pot split"
        else:
            message = f"{NAMES[dr[0]]} beats {NAMES[pr[0]]} — dealer wins"
        phase = "show"

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT and phase in {"ready", "show"}:
                    bet = max(5, bet - 5)
                elif event.key == pygame.K_RIGHT and phase in {"ready", "show"}:
                    bet = min(100, bet + 5)
                elif event.key == pygame.K_d and phase in {"ready", "show"}:
                    deal()
                elif event.key == pygame.K_RETURN and phase == "hold":
                    draw()
                elif phase == "hold" and event.unicode in "12345":
                    idx = int(event.unicode) - 1
                    hold[idx] = not hold[idx]
            elif event.type == pygame.MOUSEBUTTONDOWN and phase == "hold":
                mx, my = event.pos
                for i in range(5):
                    r = pygame.Rect(70 + i * 170, 360, 100, 144)
                    if r.collidepoint(mx, my):
                        hold[i] = not hold[i]

        screen.fill((18, 48, 32))
        pygame.draw.rect(screen, (255, 200, 70), (30, 24, W - 60, H - 48), 4, border_radius=18)
        screen.blit(title.render("FIVE-CARD DRAW", True, (255, 220, 80)), (50, 40))
        screen.blit(ui.render(f"Bank \u00a3{bank}    Bet \u00a3{bet}", True, (230, 255, 230)), (50, 90))
        screen.blit(ui.render(message, True, (180, 255, 210)), (50, 124))

        screen.blit(small.render("DEALER", True, (200, 230, 200)), (70, 170))
        if phase == "show":
            for i, card in enumerate(dealer):
                draw_card(screen, card, 70 + i * 170, 196)
            screen.blit(ui.render(NAMES[hand_rank(dealer)[0]], True, (255, 255, 255)), (70, 348))
        else:
            for i in range(5):
                box = pygame.Rect(70 + i * 170, 196, 100, 144)
                pygame.draw.rect(screen, (40, 70, 160), box, border_radius=10)
                pygame.draw.rect(screen, (255, 210, 70), box, 3, border_radius=10)

        screen.blit(small.render("YOU  (gold border = HOLD)", True, (200, 230, 200)), (70, 336 if phase != "show" else 430))
        y_you = 360
        if player:
            for i, card in enumerate(player):
                draw_card(screen, card, 70 + i * 170, y_you, selected=hold[i] and phase == "hold")
            if phase == "show":
                screen.blit(ui.render(NAMES[hand_rank(player)[0]], True, (255, 255, 255)), (70, 514))

        screen.blit(small.render("\u2190 \u2192 bet   D deal   1-5 / click hold   ENTER draw   ESC menu", True, (190, 210, 190)), (50, 590))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
