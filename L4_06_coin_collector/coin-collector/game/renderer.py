"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, player, coins,obstacles,game_over=False):
    surface.fill(COLOR_BG)
    for coin in coins:
        pygame.draw.circle(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)

    for obstacle in obstacles:
        pygame.draw.rect(surface,obstacle.color,obstacle.get_rect())

    if not game_over:
        pygame.draw.rect(surface,COLOR_PLAYER,player.get_rect(),border_radius=4)

def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)

def draw_banner(surface, font, text):

    # Make a bold version of the font
    font.set_bold(True)

    lines = text.split("\n")

    line_height = font.get_height()
    total_height = line_height * len(lines)

    start_y = (
        surface.get_height() - total_height
    ) // 2

    for i, line in enumerate(lines):

        surf = font.render(
            line,
            True,
            (255, 220, 80)
        )

        rect = surf.get_rect(
            center=(
                surface.get_width() // 2,
                start_y + i * line_height
            )
        )

        surface.blit(surf, rect)

    # Restore normal font
    font.set_bold(False)