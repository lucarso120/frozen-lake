import pygame 

def load_image(image_path, size=None):
    image = pygame.image.load(image_path)
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image