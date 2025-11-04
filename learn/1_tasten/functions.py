import pygame


def zeige_text(window, text):
    """
    Zeigt Text in der Mitte des Fensters an.

    Args:
        window: Das Pygame-Fenster
        text: Der anzuzeigende Text
    """
    font = pygame.font.Font(None, 48)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=window.get_rect().center)
    window.blit(text_surface, text_rect)
