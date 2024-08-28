# constants.py

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300  # Degrees per second
PLAYER_SPEED = 200  # Units per second
PLAYER_SHOOT_SPEED = 500  # Speed of bullets

# New constant for shooting cooldown
PLAYER_SHOOT_COOLDOWN = 0.3  # Cooldown time in seconds between shots
SHOT_RADIUS = 5
