def kollision(obj1, obj2):
    """
    Prüft, ob sich zwei Objekte überlappen.

    Args:
        obj1: Erstes Objekt (pygame.Rect)
        obj2: Zweites Objekt (pygame.Rect)

    Returns:
        True wenn sich die Objekte überlappen, sonst False
    """
    return obj1.colliderect(obj2)
