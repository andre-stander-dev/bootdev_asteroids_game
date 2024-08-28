# asteroid.py

import pygame
import random  # Import random module for generating random angles
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS, ASTEROID_SPAWN_RATE, ASTEROID_KINDS

class CircleShape(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def collides_with(self, other):
        """Check if this CircleShape collides with another CircleShape."""
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, updatable, drawable):
        super().__init__(radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)  # Default velocity
        self.updatable = updatable
        self.drawable = drawable

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt  # Move the asteroid in the direction of its velocity

    def kill(self):
        """Remove the asteroid from the game."""
        if self in self.updatable:
            self.updatable.remove(self)
        if self in self.drawable:
            self.drawable.remove(self)

    def split(self):
        """Split the asteroid into two smaller asteroids if possible."""
        self.kill()  # Remove the current asteroid

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # If the asteroid is too small, don't split further

        # Calculate new properties for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Generate a random angle for the split
        random_angle = random.uniform(20, 50)

        # Create two new velocity vectors based on the random angle
        velocity1 = self.velocity.rotate(random_angle) * 1.2  # Increase speed slightly
        velocity2 = self.velocity.rotate(-random_angle) * 1.2  # Increase speed slightly

        # Create two new smaller asteroids at the current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, self.updatable, self.drawable)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, self.updatable, self.drawable)

        # Set their velocities to the new vectors
        asteroid1.velocity = velocity1
        asteroid2.velocity = velocity2

        # Add the new asteroids to the updatable and drawable lists
        self.updatable.append(asteroid1)
        self.drawable.append(asteroid1)
        self.updatable.append(asteroid2)
        self.drawable.append(asteroid2)

class AsteroidField:
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, updatable, drawable):
        self.updatable = updatable
        self.drawable = drawable
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, self.updatable, self.drawable)
        asteroid.velocity = velocity
        self.updatable.append(asteroid)
        self.drawable.append(asteroid)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # Spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
