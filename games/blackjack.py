#!/usr/bin/env python3
"""Neon Blackjack — colourful 21 against the dealer."""

from __future__ import annotations

import random
import pygame

W, H = 960, 640
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RED_SUITS = {"\u2665", "\u2666"}


def new_deck():
    deck = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


def value(hand):
    total = 0
    aces = 0
    for r, _ in hand:
        if r == "A":
            aces += 1
            total += 11
        elif r in {"J", "Q", "K"}:
            total += 10
        else:
            total += int(r)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def draw_card(surf, card, x, y, back=False):
    rect = pygame.Rect(x, y, 92, 132)
    pygame.draw.rect(surf, (18, 18, 28), rect.inflate(6, 6), border_radius=12)
    if back or card is None:
        pygame.draw.rect(surf, (40, 70, 180), rect, border_radius=10)
        pygame.draw.rect(surf, (255, 210, 70), rect, 3, border_radius=10)
        pygame.draw.circle(surf, (255, 90, 160), rect.center, 18, 3)
        return
    rank, suit = card
    pygame.draw.rect(surf, (250, 248, 240), rect, border_radius=10)
    pygame.draw.rect(surf, (30, 30, 40), rect, 2, border_radius=10)
    colour = (200, 30, 50) if suit in RED_SUITS else (20, 20, 30)
    font = pygame.font.SysFont("arial", 26, bold=True)
    big = pygame.font.SysFont("arial", 36, bold=True)
    surf.blit(font.render(rank, True, colour), (x + 8, y + 6))
    surf.blit(font.render(suit, True, colour), (x + 8, y + 32))
    mid = big.render(suit, True, colour)
    surf.blit(mid, mid.get_rect(center=rect.center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Blackjack — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 42, bold=True)
    ui = pygame.font.SysFont("arial", 24, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 500
    bet = 25
    deck = new_deck()
    player = []
    dealer = []
    phase = "bet"
    message = "Place a bet, then DEAL"
    hide_dealer = True

    def deal_one(hand):
        nonlocal deck
        if len(deck) < 8:
            deck = new_deck()
        hand.append(deck.pop())

    def start_hand():
        nonlocal player, dealer, phase, hide_dealer, bank, message
        if bank < bet:
            message = "Not enough chips — change bet"
            return
        bank -= bet
        player, dealer = [], []
        deal_one(player)
        deal_one(dealer)
        deal_one(player)
        deal_one(dealer)
        hide_dealer = True
        phase = "play"
        if value(player) == 21:
            phase = "dealer"
            message = "Blackjack!"
        else:
            message = "HIT or STAND"

    def finish():
        nonlocal bank, phase, hide_dealer, message
        hide_dealer = False
        pv, dv = value(player), value(dealer)
        if pv > 21:
            message = "Bust — dealer wins"
        elif dv > 21 or pv > dv:
            win = int(bet * 2.5) if pv == 21 and len(player) == 2 else bet * 2
            bank += win
            message = f"You win +{win}"
        elif pv == dv:
            bank += bet
            message = "Push — bet returned"
        else:
            message = "Dealer wins"
        phase = "result"

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT and phase in {"bet", "result"}:
                    bet = max(5, bet - 5)
                elif event.key == pygame.K_RIGHT and phase in {"bet", "result"}:
                    bet = min(200, bet + 5)
                elif event.key == pygame.K_d and phase in {"bet", "result"}:
                    start_hand()
                elif event.key == pygame.K_h and phase == "play":
                    deal_one(player)
                    if value(player) >= 21:
                        phase = "dealer"
                elif event.key == pygame.K_s and phase == "play":
                    phase = "dealer"

        if phase == "dealer":
            hide_dealer = False
            while value(dealer) < 17:
                deal_one(dealer)
            finish()

        screen.fill((8, 42, 28))
        pygame.draw.rect(screen, (10, 70, 42), (40, 40, W - 80, H - 80), border_radius=24)
        pygame.draw.rect(screen, (255, 210, 70), (40, 40, W - 80, H - 80), 4, border_radius=24)
        screen.blit(title.render("NEON BLACKJACK", True, (255, 220, 80)), (60, 56))
        screen.blit(ui.render(f"Bank  \u00a3{bank}", True, (220, 255, 220)), (60, 110))
        screen.blit(ui.render(f"Bet  \u00a3{bet}", True, (255, 200, 80)), (280, 110))
        screen.blit(ui.render(message, True, (180, 255, 220)), (480, 110))

        screen.blit(small.render("DEALER", True, (200, 230, 210)), (80, 170))
        for i, card in enumerate(dealer):
            draw_card(screen, card, 80 + i * 104, 196, back=(hide_dealer and i == 1))
        if dealer:
            shown = value(dealer[:1]) if hide_dealer else value(dealer)
            screen.blit(ui.render(str(shown), True, (255, 255, 255)), (80 + len(dealer) * 104, 240))

        screen.blit(small.render("YOU", True, (200, 230, 210)), (80, 360))
        for i, card in enumerate(player):
            draw_card(screen, card, 80 + i * 104, 386)
        if player:
            screen.blit(ui.render(str(value(player)), True, (255, 255, 255)), (80 + len(player) * 104, 430))

        help_txt = "\u2190 \u2192 bet   D deal   H hit   S stand   ESC menu"
        screen.blit(small.render(help_txt, True, (180, 220, 190)), (60, H - 50))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
