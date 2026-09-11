# ElbowOS Arcade

Colourful **Python 3** mini-games built with [pygame](https://www.pygame.org/).  
Project page: **[x.com/ElbowOS](https://x.com/ElbowOS)**

These are original games — not console emulators and not ports of copyrighted titles.

## Games

| Game | What it is | Controls |
| --- | --- | --- |
| **Plumber Jump** | Side-scrolling platformer: coins, patrol enemies, flag at the end | WASD / arrows, Space jump, R restart |
| **Neon Blackjack** | Casino 21 vs the dealer | ← → bet, D deal, H hit, S stand |
| **Roulette Royale** | European wheel (0–36) | R red, B black, N / ↑↓ number, Space spin |
| **Lucky Slots** | Three-reel neon slots | ← → bet, Space spin |
| **Five-Card Draw** | Poker vs the house | D deal, 1–5 or click to hold, Enter draw |
| **Colour Memory** | Match six vivid pairs | Click cards, R restart |

## Run

```bash
python3 -m pip install -r requirements.txt
python3 arcade.py
```

Or launch one game directly:

```bash
python3 games/plumber_jump.py
python3 games/blackjack.py
python3 games/roulette.py
python3 games/slots.py
python3 games/poker.py
python3 games/memory.py
```

Needs Python 3.10+ and a desktop window (pygame + SDL).

## Notes

- No third-party sprites: everything is drawn with pygame primitives so the repo stays small and self-contained.
- “Plumber Jump” is an original platformer inspired by the *genre*, not a Mario Bros emulator.
- Casino games are for entertainment. No real-money gambling.

## Link

Follow updates: https://x.com/ElbowOS  
Source owner: https://github.com/ApacheAde
