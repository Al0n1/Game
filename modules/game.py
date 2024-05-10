"""
author: Al0n1
version: 0.0.1

:description:
Модуль содержащий классы меню и элементов меню
"""


from config import *
from colours import *
from spritesheet import SpriteSheet
import pygame
import random


class MenuItem:
    def __init__(self, menu: 'Menu', screen, rect: pygame.Rect, text: str, color: tuple, name: str = "item"):
        self.__screen = screen
        self.__rect = rect  # прямоугольник, описывающий положение и размер элемента
        self.__text = text  # текст элемента
        self.__color = color  # цвет текста
        self.__name = name
        self.__menu = menu
        if self.__menu is not None:
            self.assign_button_to_menu()

    def assign_button_to_menu(self):
        self.__menu.add_item(self)

    def display(self):
        # Отображение элемента на экране
        pygame.draw.rect(self.__screen, (255, 255, 255), self.__rect, border_radius=5)  # пример отображения элемента как прямоугольника
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(self.__text, True, self.__color)
        text_rect = text_surface.get_rect(center=self.__rect.center)
        self.__screen.blit(text_surface, text_rect)

    def click_action(self):
        # Действие, выполняемое при клике на элемент
        if self.__name == 'start':
            print("Start!")
            interface = self.__menu.get_interface()
            interface.switch_menu(self.__menu.get_next_menu())
        elif self.__name == 'end':
            print("end")
            self.__menu.change_status(False)
            pygame.quit()

    def get_rect(self) -> pygame.Rect:
        return self.__rect


class Menu:
    def __init__(self, screen, player_interface):
        self.__screen = screen
        self.__menu_items: list[MenuItem] = []
        self.__running: bool = True
        self.__next_menu = None
        self.__prev_menu = None
        self.__interface = player_interface
        self.__background_color: tuple = WHITE

    def add_item(self, item: MenuItem):
        self.__menu_items.append(item)

    def get_menu_items(self) -> list[MenuItem]:
        return self.__menu_items

    def get_screen(self):
        return self.__screen

    def display_menu_items(self):
        for item in self.__menu_items:
            item.display()

    def handle_click(self, pos):
        for item in self.__menu_items:
            if item.get_rect().collidepoint(pos):
                item.click_action()

    def get_status(self) -> bool:
        return self.__running

    def change_status(self, status: bool = None):
        self.__running = not self.__running if status is None else status

    def initialize_buttons(self):
        pass

    def set_next_menu(self, menu):
        self.__next_menu = menu

    def set_prev_menu(self, menu):
        self.__prev_menu = menu
        menu.set_next_menu(self)

    def get_next_menu(self):
        return self.__next_menu

    def get_prev_menu(self):
        return self.__prev_menu

    def get_interface(self):
        return self.__interface

    def get_background_color(self):
        return self.__background_color

    def set_background_color(self, color):
        self.__background_color = color


class PlayerInterface:
    def __init__(self, menus: dict = {}):
        self.__current_menu = None
        self.__menus: dict = menus

    def switch_menu(self, menu: str | object = None):
        if isinstance(menu, str) and menu is not None:
            self.__current_menu = self.__menus[menu]
        elif isinstance(menu, object) and menu is not None:
            self.__current_menu = menu
        else:
            self.__current_menu = None

    def get_current_menu(self) -> dict:
        return self.__current_menu

    def get_menu(self, name: str) -> object:
        return self.__menus[name]

    def set_menus(self, menus: dict):
        self.__menus = menus


class MainMenu(Menu):
    def __init__(self, screen, player_interface):
        super().__init__(screen, player_interface)

        self.initialize_buttons()

    def initialize_buttons(self):
        button1_x = (SCREEN_WIDTH - MAIN_MENU_BUTTON_WIDTH) // 2
        button1_y = (SCREEN_HEIGHT - MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

        button2_x = button1_x
        button2_y = button1_y + MAIN_MENU_BUTTON_HEIGHT + 30

        # Инициализация кнопки "Начать игру"
        MenuItem(self, self.get_screen(),
                 pygame.Rect(button1_x, button1_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                 "Начать игру",
                 (0, 0, 0),
                 "start")

        # Инициализация кнопки "Выход"
        MenuItem(self, self.get_screen(),
                 pygame.Rect(button2_x, button2_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                 "Выход",
                 (0, 0, 0),
                 "end")


class ClickerMenu(Menu):
    def __init__(self, screen, main_menu, player_interface):
        super().__init__(screen, player_interface)

        self.set_prev_menu(main_menu)
        self.initialize_items()

    def initialize_items(self):
        button1_x = (SCREEN_WIDTH - CLICKER_MENU_BUTTON_WIDTH) // 2
        button1_y = (SCREEN_HEIGHT - CLICKER_MENU_BUTTON_HEIGHT) // 2

        button2_x = button1_x + CLICKER_MENU_BUTTON_WIDTH
        button2_y = button1_y

        # Инициализация кнопки "Улучшения кликов"
        MenuItem(self, self.get_screen(),
                 pygame.Rect(button1_x, button1_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                 "Улучшения кликов",
                 (0, 0, 0),
                 "start")

        # Инициализация кнопки "Выход"
        MenuItem(self, self.get_screen(),
                 pygame.Rect(button2_x, button2_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                 "Выход",
                 (0, 0, 0),
                 "end")


class AutoClickerMenu:
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class MonsterSprite(pygame.sprite.Sprite):
    """
    Класс спрайта монстра
    """
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Загружаем изображение монстра
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Monster:
    """
    Класс для отображения монстра
    """
    def __init__(self, screen, x, y, width, height, color):
        self.__screen = screen
        self.__rect = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__health = 10  # Здоровье монстра
        self.__monster_name = None
        self.__filename_of_sprite = None
        self.__sprite = None

        self.change_monster()

    def draw(self):
        """
        Отрисовка монстра
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Health: {self.health}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        self.screen.blit(text_surface, text_rect)

    def handle_click(self):
        pass

    def change_monster(self, monster_name: str = random.choice(MONSTERS_IN_CLICKER)):
        self.__monster_name = monster_name
        self.__filename_of_sprite = self.__monster_name + "_sheet_idle.png"
        self.__sprite = SpriteSheet(self.__filename_of_sprite)

    def change_monster_state(self, state):
        """
        Функция изменяет состояние текущего монстра, например монстр атакует или получает урон
        :param state:
        :return:
        """
        pass

    def set_hp_to_monster(self):
        pass


class Player:
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
