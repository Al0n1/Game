__author__ = "Al0n1"
__version__ = "0.0.4"


import json
import pygame

from colors import *


class SpriteSheet:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__sprite_sheet = pygame.image.load(f"../Game/sprites/zombies/{filename}").convert_alpha()
        with open("../Game/sprites/sprite_sheet.json", "r") as file:
            filename = filename[:filename.find('_')]
            self.__data = json.load(file)['frames'][filename]

    def _get_sprite(self, x: int, y: int, width: int, height: int, scale: int) -> pygame.Surface:
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey(BLACK)
        sprite.blit(self.__sprite_sheet, (0, 0), (x, y, width, height))
        sprite = pygame.transform.scale(sprite, (width * scale, height * scale))
        return sprite

    def parse_sprite(self, state: str, sprite_index: int = 1, scale: int = 1) -> pygame.Surface:
        sprite = self.__data[state][f'frame_{sprite_index}']['frame']
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self._get_sprite(x=x, y=y, width=width, height=height, scale=scale)
        return image

    def get_data(self) -> dict:
        return self.__data
