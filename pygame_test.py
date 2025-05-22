import sys
import time

print("Starting Pygame test...")
print(f"Python version: {sys.version}")

try:
    print("Attempting to import pygame...")
    import pygame
    print(f"Pygame successfully imported. Version: {pygame.version.ver}")
    
    print("Attempting to initialize pygame...")
    pygame.init()
    init_result = pygame.init()
    print(f"Pygame initialization result: {init_result}")
    
    print("Attempting to create a small display...")
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('Pygame Test')
    print("Display created successfully!")
    
    # Fill the screen with white
    screen.fill((255, 255, 255))
    pygame.display.update()
    print("Screen updated with white background")
    
    # Wait for 3 seconds
    print("Waiting for 3 seconds...")
    time.sleep(3)
    
    print("Test completed successfully!")
    pygame.quit()
    
except ImportError as e:
    print(f"ERROR: Failed to import pygame: {e}")
    print("Please install pygame with: pip install pygame")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: An unexpected error occurred: {e}")
    if 'pygame' in sys.modules:
        pygame.quit()
    sys.exit(1)