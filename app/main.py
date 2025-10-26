import pygame
import asyncio

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 10, 10)
rect.center = window.get_rect().center
vel = 5


async def main():
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))

        keys = pygame.key.get_pressed()

        rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
        rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

        # Keep the square inside the window by wrapping around
        rect.centerx = rect.centerx % window.get_width()
        rect.centery = rect.centery % window.get_height()

        window.fill(0)
        pygame.draw.rect(window, "red", rect)
        pygame.display.flip()
        await asyncio.sleep(0)  # required for pygbag

    pygame.quit()
    exit()


# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
