# player.py

import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from asteroid import CircleShape  # Import the CircleShape class
from shot import Shot  # Import the Shot class

class Player(CircleShape):  # Inherit from CircleShape
    def __init__(self, x, y, shots, updatable, drawable):
        super().__init__(PLAYER_RADIUS)  # Initialize the CircleShape with PLAYER_RADIUS
        self.position = pygame.Vector2(x, y)  # Player's position
        self.rotation = 0  # Initial rotation
        self.shots = shots  # Reference to the shots list
        self.shoot_timer = 0  # Initialize the shooting cooldown timer
        self.updatable = updatable  # Reference to the updatable list
        self.drawable = drawable  # Reference to the drawable list

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        """Rotate the player by PLAYER_TURN_SPEED * dt."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        """Move the player in the direction it is facing."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # Direction vector
        self.position += forward * PLAYER_SPEED * dt  # Update position

    def shoot(self):
        """Create a new shot at the player's position and set its velocity."""
        if self.shoot_timer <= 0:  # Check if the timer has expired
            shot = Shot(self.position.x, self.position.y, self.updatable, self.drawable)  # Pass updatable and drawable
            forward = pygame.Vector2(0, 1).rotate(self.rotation)  # Direction vector
            shot.velocity = forward * PLAYER_SHOOT_SPEED  # Set shot's speed
            self.shots.append(shot)  # Add the shot to the shots list
            self.updatable.append(shot)  # Also add the shot to the updatable list
            self.drawable.append(shot)  # Also add the shot to the drawable list
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN  # Reset the cooldown timer

    def update(self, dt):
        """Update player state."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:  # Rotate left
            self.rotate(-dt)  # Negative for left rotation
        if keys[pygame.K_d]:  # Rotate right
            self.rotate(dt)   # Positive for right rotation
        if keys[pygame.K_w]:  # Move forward
            self.move(dt)
        if keys[pygame.K_s]:  # Move backward
            self.move(-dt)  # Negative for moving backward
        if keys[pygame.K_SPACE]:  # Shoot bullet
            self.shoot()

        # Decrease the cooldown timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
