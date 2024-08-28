# main.py

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid, AsteroidField
from shot import Shot  # Import Shot

def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create groups for updatable and drawable objects
    global updatable, drawable
    updatable = []  # List of objects that need to be updated
    drawable = []   # List of objects that need to be drawn
    shots = []      # List of all shots

    # Create a Player instance in the middle of the screen and pass the shots list
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y, shots, updatable, drawable)  # Pass updatable and drawable lists to Player

    updatable.append(player)
    drawable.append(player)

    # Create the AsteroidField
    asteroid_field = AsteroidField(updatable, drawable)
    updatable.append(asteroid_field)  # Add the asteroid field to the updatable group

    dt = 0  # Delta time between frames
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Update all updatable objects
        for obj in updatable + shots:  # Include shots in the update
            obj.update(dt)

        # Check for collisions between player and asteroids
        for obj in updatable:
            if isinstance(obj, Asteroid):  # Check if the object is an asteroid
                if player.collides_with(obj):
                    print("Game over!")
                    pygame.quit()
                    return

        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in updatable:
                if isinstance(asteroid, Asteroid):
                    if shot.collides_with(asteroid):
                        shot.kill()  # Remove shot
                        asteroid.split()  # Split the asteroid instead of killing
                        print("Asteroid destroyed!")

        # Clear the screen
        screen.fill('black')

        # Draw all drawable objects
        for obj in drawable + shots:  # Include shots in the draw
            obj.draw(screen)

        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate at 60 FPS and get delta time
        dt = clock.tick(60) / 1000  # Converts milliseconds to seconds

if __name__ == "__main__":
    main()
