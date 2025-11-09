import pygame
import asyncio
import logging
#from functions import kollision

logger = logging.getLogger("pygame")

pygame.init()
window = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


async def main():
    """
    Pygame Tutorial 2: Bewegung mit Tasten
    """

    run = True

    # Bewegbares Objekt aus einem Bild
    obj = pygame.image.load("images/pacman.png")
    # Größe verändern
    obj = pygame.transform.scale(obj, (50, 50))
    # Position des Objekts
    position = obj.get_rect(center=window.get_rect().center)
    # Rotierte Version des Objekts (anfangs unverändert)
    #obj_rotiert = obj

    # Wand
    wand = pygame.Rect(150, 100, 100, 20)

    # Keine Taste gedrückt
    taste = ""

    # Ist ein Tasten-Event erfolgt
    #tastenwechsel = False

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Get the name of the pressed key
                taste = pygame.key.name(event.key)
                #tastenwechsel = True
                logger.info(f"Taste: {taste}")

        # Blauer Hintergrund
        window.fill((20, 20, 100))

        # Aufgabe 1:
        # Abfragen, ob Tasten gedrückt sind
        # "left", "right", "up", "down"
        # Logik wenn Taste "right" ist, erhöhe position.x um 1

        # Aufgabe 2:
        # Zeichne die Wand als rotes Rechteck
        pygame.draw.rect(window, (200, 0, 0), wand)
        # Prüfe mit der Funktion kollision, ob obj die Wand berührt
        # Nutze dafür die Funktion kollisition(object1, object2) <- oben auskommentiert
        # Wenn eine Kollision erkannt wird, bewege das obj zurück und stoppe die
        # Bewegung


        # Aufgabe 2:
        # Je nach Richtung soll das Objekt gedreht werden
        # wenn ein Tastenwechsel erfolgt ist
        # Nutze dazu obj_rotiert und tastenwechsel (auskommentierte Befehle)

        # Zeige obj an der aktuellen Position
        window.blit(obj, position)

        #tastenwechsel = False

        pygame.display.flip()
        await asyncio.sleep(0)  # required for pygbag

    pygame.quit()
    exit()


# This is the program entry point:
asyncio.run(main())
