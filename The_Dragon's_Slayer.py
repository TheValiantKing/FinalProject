import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set window dimensions
    window_width = 800
    window_height = 600

    # Create a resizable window
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Resizable Pygame Window")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Adjust the screen size to the new window dimensions
                window_width, window_height = event.size
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

        # Fill the screen with a color
        screen.fill((0, 0, 0))  # Black

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()