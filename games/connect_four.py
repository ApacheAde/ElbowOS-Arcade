#!/usr/bin/env python3
"""Connect Four — colourful two-player / vs-bot board game."""

from __future__ import annotations

import random
import pygame

W, H = 840, 720
COLS, ROWS = 7, 6
CELL = 88
OX, OY = 112, 120
RED = (230, 60, 80)
YEL = (255, 210, 50)
NAVY = (18, 28, 72)
CYAN = (70, 220, 255)
WHITE = (250, 250, 255)


def drop(board, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = piece
            return r
    return -1


def winner(board):
    for r in range(ROWS):
        for c in range(COLS):
            p = board[r][c]
            if not p:
                continue
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = []
                for i in range(4):
                    rr, cc = r + dr * i, c + dc * i
                    if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == p:
                        cells.append((rr, cc))
                    else:
                        break
                if len(cells) == 4:
                    return p, cells
    if all(board[0][c] for c in range(COLS)):
        return 3, []
    return 0, []


def bot_move(board):
    legal = [c for c in range(COLS) if board[0][c] == 0]
    if not legal:
        return 0
    for piece in (2, 1):
        for c in legal:
            clone = [row[:] for row in board]
            drop(clone, c, piece)
            if winner(clone)[0] == piece:
                return c
    mid = [c for c in (3, 2, 4, 1, 5, 0, 6) if c in legal]
    return mid[0] if mid else random.choice(legal)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Connect Four — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 46, bold=True)

    board = [[0] * COLS for _ in range(ROWS)]
    turn = 1
    vs_bot = True
    over = 0
    line = []
    hover = 3
    anim = None

    running = True
    while running:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        hover = max(0, min(COLS - 1, (mx - OX) // CELL))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    board = [[0] * COLS for _ in range(ROWS)]
                    turn, over, line, anim = 1, 0, [], None
                elif event.key == pygame.K_b:
                    vs_bot = not vs_bot
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    hover = (hover - 1) % COLS
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    hover = (hover + 1) % COLS
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN) and not over and anim is None:
                    if board[0][hover] == 0:
                        row = drop(board, hover, turn)
                        anim = (hover, -1.0, row, turn)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not over and anim is None:
                if board[0][hover] == 0:
                    row = drop(board, hover, turn)
                    anim = (hover, -1.0, row, turn)

        if anim:
            c, y, target, piece = anim
            y += 0.35
            if y >= target:
                anim = None
                over, line = winner(board)
                if not over:
                    turn = 3 - turn
                    if vs_bot and turn == 2:
                        c2 = bot_move(board)
                        row = drop(board, c2, 2)
                        anim = (c2, -1.0, row, 2)
            else:
                anim = (c, y, target, piece)

        screen.fill((10, 14, 36))
        screen.blit(big.render("CONNECT FOUR", True, CYAN), (40, 18))
        mode = "You vs Bot  (B to toggle)" if vs_bot else "Hot-seat 2P  (B to toggle)"
        screen.blit(font.render(mode + "   R restart   ESC menu", True, WHITE), (40, 72))

        pygame.draw.rect(screen, (30, 80, 200), (OX - 16, OY - 16, COLS * CELL + 32, ROWS * CELL + 32), border_radius=18)
        for r in range(ROWS):
            for c in range(COLS):
                cx = OX + c * CELL + CELL // 2
                cy = OY + r * CELL + CELL // 2
                val = board[r][c]
                if anim and c == anim[0] and r == anim[2]:
                    val = 0
                col = (20, 30, 70) if val == 0 else (RED if val == 1 else YEL)
                pygame.draw.circle(screen, col, (cx, cy), 34)
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 34, 2)
                if (r, c) in line:
                    pygame.draw.circle(screen, WHITE, (cx, cy), 38, 4)

        if anim:
            c, y, _, piece = anim
            cy = OY + y * CELL + CELL // 2
            pygame.draw.circle(screen, RED if piece == 1 else YEL, (OX + c * CELL + CELL // 2, int(cy)), 34)

        if not over and anim is None:
            pygame.draw.circle(screen, RED if turn == 1 else YEL, (OX + hover * CELL + CELL // 2, OY - 48), 22)

        if over == 1:
            msg = "RED WINS"
        elif over == 2:
            msg = "YELLOW WINS"
        elif over == 3:
            msg = "DRAW"
        else:
            msg = "RED to play" if turn == 1 else "YELLOW to play"
        screen.blit(font.render(msg, True, YEL if over else WHITE), (W // 2 - 80, H - 40))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
