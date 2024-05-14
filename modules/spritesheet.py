"""
author: Al0n1
version: 0.0.2

:description:
Модуль содержит класс листа спрайтов. Этот класс содержит функции позволяющие выделить из листа
один спрайт из всей последовательности
"""


import json
import pygame


class SpriteSheet:
    """
    Класс последовательности(лист) спрайтов.
    """
    def __init__(self, filename: str, state: str = "idle"):
        """
        :param filename: название файла последовательности
        :param state: состояние объекта на спрайте
        """
        self.__filename = filename
        self.__sprite_sheet = pygame.image.load(f"../Game/sprites/zombies/{filename}").convert_alpha()
        with open("../Game/sprites/sprite_sheet.json", "r") as file:
            filename = filename[:filename.find('_')]
            self.__data = json.load(file)['frames'][filename]
        self.__last_tick = pygame.time.get_ticks()
        self.__cooldown = 100
        self.__state = state

    # <editor-fold desc="Функции для получения спрайта">
    def _get_sprite(self, x: int, y: int, w: int, h: int, scale: int) -> pygame.Surface:
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
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.__sprite_sheet, (0, 0), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (w * scale, h * scale))
        return sprite

    def parse_sprite(self, sprite_index: int = 1, scale: int = 1) -> pygame.Surface:
        """
        Функция находит нужный спрайт и его параметры в метаданных
        :param sprite_index: номер слайда в последовательности
        :param scale: множитель размера спрайта
        :return: поверхность pygame со спрайтом
        """
        sprite = self.__data[self.__state][f'frame_{sprite_index}']['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self._get_sprite(x, y, w, h, scale)
        return image
    # </editor-fold>

    def can_change_sprite(self) -> bool:
        """
        Функция проверяет прошло ли достаточно времени для смены кадра спрайта
        :return: True/False
        """
        now = pygame.time.get_ticks()
        if now - self.__last_tick >= self.__cooldown:
            self.__last_tick = now
            return True
        else:
            return False

    # <editor-fold desc="Функции и методы для работы с переменными класса">
    def get_data(self) -> dict:
        """
        :return: словарь с метаданными последовательности спрайтов
        """
        return self.__data

    def set_cooldown(self, value: int):
        """
        Устанавливает задержку в смене кадров анимации спрайта
        :param value: значение в мс, через какое время должна произойти смена кадра анимации спрайта
        """
        self.__cooldown = value
    # </editor-fold>
