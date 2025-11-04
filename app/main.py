import pygame
import asyncio

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 25, 25)
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

        # Move horizontally
        if keys[pygame.K_RIGHT]:
            rect.x += vel
        elif keys[pygame.K_LEFT]:
            rect.x -= vel

        # Move vertically
        if keys[pygame.K_DOWN]:
            rect.y += vel
        elif keys[pygame.K_UP]:
            rect.y -= vel

        # Keep the square inside the window by wrapping around
        rect.centerx = rect.centerx % window.get_width()
        rect.centery = rect.centery % window.get_height()

        window.fill(0)
        pygame.draw.rect(window, "white", rect)
        pygame.display.flip()
        await asyncio.sleep(0)  # required for pygbag

    pygame.quit()
    exit()


# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
