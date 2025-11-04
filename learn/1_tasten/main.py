import pygame
import asyncio
from functions import zeige_text

pygame.init()
window = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


async def main():
    """
    Pygame Tutorial 1: Keyboard Input
    Displays which key is being pressed in the center of the screen.
    """
    current_key = "Press any key..."

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Get the name of the pressed key
                current_key = f"Taste: {pygame.key.name(event.key)}"
                print(f"Taste: {pygame.key.name(event.key)}")

        # Clear screen with dark blue background
        window.fill((20, 20, 60))

        # Render and display the current key text
        zeige_text(window, current_key)

        pygame.display.flip()
        await asyncio.sleep(0)  # required for pygbag

    pygame.quit()
    exit()


# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
