"""
Модуль содержащий классы игры
"""

import pygame
from config import *


class MenuItem:
    def __init__(self, menu: object, screen, rect: pygame.Rect, text: str, color: tuple, name: str = "item"):
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
        elif self.__name == 'end':
            print("end")
            self.__menu.change_status()
            pygame.quit()

    def get_rect(self) -> pygame.Rect:
        return self.__rect


class Menu:
    def __init__(self, screen):
        self.__screen = screen
        self.__menu_items: list[MenuItem] = []
        self.__running: bool = True

    def add_item(self, item: MenuItem):
        self.__menu_items.append(item)

    def get_menu_items(self) -> list[MenuItem]:
        return self.__menu_items

    def get_screen(self):
        return self.__screen

    def display_menu(self):
        for item in self.__menu_items:
            item.display()

    def handle_click(self, pos):
        for item in self.__menu_items:
            if item.get_rect().collidepoint(pos):
                item.click_action()

    def get_status(self) -> bool:
        return self.__running

    def change_status(self):
        self.__running = not self.__running


class PlayerInterface:
    def __init__(self, menus: dict):
        self.__current_menu = None
        self.__menus: dict = menus

    def switch_menu(self, menu: str | object = None):
        if type(menu) == str and menu is not None:
            self.__current_menu = self.__menus[menu]
        elif type(menu) == object and menu is not None:
            self.__current_menu = menu
        else:
            self.__current_menu = None

    def get_current_menu(self) -> dict:
        return self.__current_menu

    def get_menu(self, name: str) -> object:
        return self.__menus[name]


class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

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


class UpgradeButton:
    def __init__(self, screen, x, y, width, height, color, text, click_action):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.click_action = click_action

    def draw(self):
        """

        :return:
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

    def handle_click(self):
        """

        :return:
        """
        self.click_action()


class ClickerMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.initialize_buttons()


    def initialize_buttons(self):
        button1_x = (SCREEN_WIDTH - MAIN_MENU_BUTTON_WIDTH) // 2
        button1_y = (SCREEN_HEIGHT - MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

        button2_x = button1_x
        button2_y = button1_y + MAIN_MENU_BUTTON_HEIGHT + 30

        # Инициализация кнопки "Начать игру"
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


class Monster:
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class Player:
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
