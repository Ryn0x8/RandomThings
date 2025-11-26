import pygame
import random
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 300, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Dice Roller")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DICE_SIZE = 200
PIP_RADIUS = 12

# Pip positions (relative to dice square)
def get_pip_positions():
    margin = DICE_SIZE * 0.2
    c = DICE_SIZE / 2
    left = margin
    right = DICE_SIZE - margin
    top = margin
    bottom = DICE_SIZE - margin

    return {
        "tl": (left, top),
        "tc": (c, top),
        "tr": (right, top),
        "cl": (left, c),
        "cc": (c, c),
        "cr": (right, c),
        "bl": (left, bottom),
        "bc": (c, bottom),
        "br": (right, bottom),
    }

PIP_POS = get_pip_positions()

PIP_MAP = {
    1: ("cc",),
    2: ("tl", "br"),
    3: ("tl", "cc", "br"),
    4: ("tl", "tr", "bl", "br"),
    5: ("tl", "tr", "cc", "bl", "br"),
    6: ("tl", "tr", "cl", "cr", "bl", "br"),
}

def draw_die(value):
    WIN.fill((180, 180, 180))

    # Draw dice background
    dice_x = (WIDTH - DICE_SIZE) // 2
    dice_y = (HEIGHT - DICE_SIZE) // 2

    pygame.draw.rect(WIN, WHITE, (dice_x, dice_y, DICE_SIZE, DICE_SIZE), border_radius=20)

    # Draw pips
    for key in PIP_MAP[value]:
        px, py = PIP_POS[key]
        pygame.draw.circle(WIN, BLACK, (int(px + dice_x), int(py + dice_y)), PIP_RADIUS)

    pygame.display.update()


def roll_animation():
    # Quick animation
    for _ in range(10):
        temp = random.randint(1, 6)
        draw_die(temp)
        pygame.time.delay(80)

    return random.randint(1, 6)


# --- Main loop ---
current_value = 1
draw_die(current_value)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Roll on click or keypress
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key not in (pygame.K_SPACE, pygame.K_RETURN):
                    continue

            current_value = roll_animation()
            draw_die(current_value)
