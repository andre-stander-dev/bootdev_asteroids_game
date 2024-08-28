# shot.py

import pygame
from asteroid import CircleShape  # Import the CircleShape class
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y, updatable, drawable):
        super().__init__(SHOT_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)  # Default velocity
        self.updatable = updatable
        self.drawable = drawable
        self.image = pygame.Surface((SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.position += self.velocity * dt  # Move the shot in the direction of its velocity
        self.rect.center = self.position  # Update rect position

    def kill(self):
        """Remove the shot from the game."""
        if self in self.updatable:
            self.updatable.remove(self)
        if self in self.drawable:
            self.drawable.remove(self)
