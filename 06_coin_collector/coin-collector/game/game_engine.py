"""
GameEngine: owns the player and all coins.

Starter version: one coin type, no obstacles, no timer yet. Coin
collection also has a known bug (see how `update` uses check_collection
below) that Task 1 asks you to fix - collected coins are never removed,
so standing on one keeps awarding points every frame.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT
from game.obstacle import Obstacle

NUM_COINS = 6
COIN_TYPES = [
    {"color": (205, 127, 50), "value": 1},   # Bronze
    {"color": (192, 192, 192), "value": 3},  # Silver
    {"color": (255, 215, 0), "value": 5}     # Gold
]

NUM_OBSTACLES = 5
STARTING_LIVES = 3
GAME_DURATION = 30
COLLISION_COOLDOWN = 2000 

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)

        self.coins = [
            self._random_coin()
            for _ in range(NUM_COINS)
        ]

        self.obstacles = [
            self._random_obstacle()
            for _ in range(NUM_OBSTACLES)
        ]

        self.score = 0

        # Lives
        self.lives = STARTING_LIVES

        # Timer
        self.start_time = pygame.time.get_ticks()
        self.time_left = GAME_DURATION

        # Collision immunity
        self.invulnerable_until = 0

        # Game state
        self.game_over = False

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)

        coin_type = random.choice(COIN_TYPES)

        return Coin(x=x, y=y, radius=12, value=coin_type["value"], color=coin_type["color"])

    def _random_obstacle(self):
        width = 40
        height = 40

        while True:
            x = random.randint(
                width // 2,
                WIDTH - width // 2
            )

            y = random.randint(
                height // 2,
                HEIGHT - height // 2
            )

            obstacle = Obstacle(
                x=x,
                y=y,
                width=width,
                height=height
            )

            if not obstacle.get_rect().colliderect(
                self.player.get_rect()
            ):
                return obstacle

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        # Don't update anything after game over
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()

        # -------------------------
        # Update countdown
        # -------------------------
        elapsed_seconds = (
            current_time - self.start_time
        ) // 1000

        self.time_left = max(
            0,
            GAME_DURATION - elapsed_seconds
        )

        # Timer reached zero
        if self.time_left <= 0:
            self.end_game()
            return

        # -------------------------
        # Check coin collection
        # -------------------------
        collected = check_collection(
            self.player,
            self.coins
        )

        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

    # -------------------------
    # Check obstacle collision
    # -------------------------

    # Only check collision if the
    # 5-second immunity period is over
        if current_time >= self.invulnerable_until:

            player_rect = self.player.get_rect()

            for obstacle in self.obstacles:

                if player_rect.colliderect(
                    obstacle.get_rect()
                ):
                    self.lives -= 1

                    # Player has no lives remaining
                    if self.lives <= 0:
                        self.end_game()
                        return

                    # Give player 5 seconds of immunity
                    self.invulnerable_until = (
                        current_time + COLLISION_COOLDOWN
                    )

                    break
    def end_game(self):
        self.game_over = True

        # Remove all sprites
        self.coins.clear()
        self.obstacles.clear()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins,self.obstacles, self.game_over)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface,font,f"Lives left: {self.lives}",(150, 10))
        renderer.draw_text(surface,font,f"Time left: {self.time_left}",(320,10))
        if self.game_over:
            renderer.draw_banner(surface,font,f"GAME OVER\nScore: {self.score}\nPress R to Restart")
