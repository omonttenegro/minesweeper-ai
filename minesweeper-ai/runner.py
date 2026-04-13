import math
import sys
import time
from array import array

import pygame

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8

# Cozy dark palette
BACKGROUND = (38, 32, 28)
TILE_LIGHT = (64, 52, 45)
TILE_DARK = (53, 44, 38)
TILE_BORDER = (94, 78, 67)
TEXT_PRIMARY = (222, 206, 189)
TEXT_ACCENT = (196, 160, 128)
BUTTON_FILL = (72, 58, 50)
BUTTON_BORDER = (132, 101, 82)
STATUS_WIN = (141, 171, 138)
STATUS_LOSE = (156, 84, 84)

# Pygame setup
pygame.init()
clock = pygame.time.Clock()

# Audio (click sound)
try:
    pygame.mixer.init()
    MIXER_AVAILABLE = True
except pygame.error:
    MIXER_AVAILABLE = False


def generate_click_tone(frequency=320, duration=0.12, volume=0.25):
    sample_rate = 44100
    amplitude = int(32767 * volume)
    total_samples = int(sample_rate * duration)
    samples = array("h")
    for n in range(total_samples):
        t = n / sample_rate
        envelope = (1 - n / total_samples) ** 2
        tone = math.sin(2 * math.pi * frequency * t)
        overtone = 0.4 * math.sin(2 * math.pi * frequency * 1.5 * t)
        value = int(amplitude * envelope * (tone + overtone))
        samples.append(value)
    return pygame.mixer.Sound(buffer=samples.tobytes())


click_sound = generate_click_tone() if MIXER_AVAILABLE else None


def play_click():
    if click_sound:
        click_sound.play()


size = width, height = 1000, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")

# Fonts
smallFont = pygame.font.SysFont("arial", 35)
mediumFont = pygame.font.SysFont("arial", 52)
largeFont = pygame.font.SysFont("arial", 70)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True


def draw_button(surface, rect, text):
    pygame.draw.rect(surface, BUTTON_FILL, rect, border_radius=12)
    pygame.draw.rect(surface, BUTTON_BORDER, rect, width=2, border_radius=12)
    label = smallFont.render(text, True, TEXT_PRIMARY)
    labelRect = label.get_rect(center=rect.center)
    surface.blit(label, labelRect)


while True:
    clock.tick(60)

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BACKGROUND)

    # Show game instructions
    if instructions:

        title = largeFont.render("Play Minesweeper", True, TEXT_PRIMARY)
        titleRect = title.get_rect(center=(width / 2, height * 0.18))
        screen.blit(title, titleRect)

        subtitle = smallFont.render("by André Montenegro", True, TEXT_ACCENT)
        subtitleRect = subtitle.get_rect(center=(width / 2, height * 0.28))
        screen.blit(subtitle, subtitleRect)

        instructions_lines = [
            "Left-click: revelar | Right-click: marcar mina",
            "Marca todas as minas para vencer!"
        ]
        for idx, line in enumerate(instructions_lines):
            text_surface = smallFont.render(line, True, TEXT_PRIMARY)
            text_rect = text_surface.get_rect(center=(width / 2, height * 0.4 + idx * 45))
            screen.blit(text_surface, text_rect)

        buttonRect = pygame.Rect((width / 2) - 150, height * 0.65, 300, 60)
        draw_button(screen, buttonRect, "Play Game")

        # Check clicks
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse_pos = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse_pos):
                play_click()
                instructions = False
                time.sleep(0.2)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            color = TILE_LIGHT if (i + j) % 2 == 0 else TILE_DARK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, TILE_BORDER, rect, 2)

            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, TEXT_ACCENT
                )
                neighborsRect = neighbors.get_rect(center=rect.center)
                screen.blit(neighbors, neighborsRect)

            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    draw_button(screen, aiButton, "AI Move")

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    draw_button(screen, resetButton, "Reset")

    # Display text
    status = ""
    status_color = TEXT_ACCENT
    if lost:
        status = "Lost"
        status_color = STATUS_LOSE
    elif game.mines == flags and len(flags) == MINES:
        status = "Won"
        status_color = STATUS_WIN

    if status:
        status_text = mediumFont.render(status, True, status_color)
        statusRect = status_text.get_rect(center=((5 / 6) * width, (2 / 3) * height))
        screen.blit(status_text, statusRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    play_click()
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        if aiButton.collidepoint(mouse) and not lost:
            play_click()
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        elif resetButton.collidepoint(mouse):
            play_click()
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)
                        play_click()

    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
