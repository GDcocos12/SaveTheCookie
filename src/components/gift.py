import pygame
from pygame.locals import *

from src.config import Config
from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2


class Gift(pygame.sprite.Sprite):
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, x, y):
        super().__init__()

        self.image = VisualizationService.get_gift_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
