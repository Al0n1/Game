"""
author: Al0n1
version: 0.0.3

:description:
Модуль содержит класс листа спрайтов. Этот класс содержит функции позволяющие выделить из листа
один спрайт из всей последовательности
"""


import json
import pygame
from colours import *


class SpriteSheet:
    """
    Класс последовательности(лист) спрайтов.
    """
    def __init__(self, filename: str):
        """
        :param filename: название файла последовательности
        :param state: состояние объекта на спрайте
        """
        self.__filename = filename
        self.__sprite_sheet = pygame.image.load(f"../Game/sprites/zombies/{filename}").convert_alpha()
        with open("../Game/sprites/sprite_sheet.json", "r") as file:
            filename = filename[:filename.find('_')]
            self.__data = json.load(file)['frames'][filename]

    def _get_sprite(self, x: int, y: int, w: int, h: int, scale: int, pos: tuple) -> pygame.Surface:
        """
        Функция создаёт поверхность pygame и выводит на неё спрайт
        :param x: координата левого верхнего края спрайта по оси x
        :param y: координата левого верхнего края спрайта по оси y
        :param w: ширина спрайта
        :param h: высота спрайта
        :param scale: множитель размера спрайта
        :return: поверхность pygame со спрайтом
        """
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey(BLACK)
        sprite.blit(self.__sprite_sheet, (0,0), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (w * scale, h * scale))
        return sprite

    def parse_sprite(self, state: str, pos: tuple, sprite_index: int = 1, scale: int = 1) -> pygame.Surface:
        """
        Функция находит нужный спрайт и его параметры в метаданных
        :param state: состояние монстра для отображения
        :param sprite_index: номер слайда в последовательности
        :param scale: множитель размера спрайта
        :return: поверхность pygame со спрайтом
        """
        sprite = self.__data[state][f'frame_{sprite_index}']['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self._get_sprite(x, y, w, h, scale, pos)
        return image

    def get_data(self) -> dict:
        """
        :return: словарь с метаданными последовательности спрайтов
        """
        return self.__data
