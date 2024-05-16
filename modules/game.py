"""
author: Al0n1
version: 0.0.3

:description:
Модуль содержащий классы меню и элементов меню
"""


from config import *
from colours import *
from spritesheet import SpriteSheet
import pygame
import random


# <editor-fold desc="Классы меню">
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

        self.add_item(Monster(self.get_screen()))


class AutoClickerMenu:
    def display_menu(self):
        pass

    def handle_click(self):
        pass
# </editor-fold>


# <editor-fold desc="Классы монстров">
class Monster:
    """
    Класс для отображения монстра
    """
    def __init__(self, screen):
        self.__screen: pygame.Surface = screen
        self.__pos: tuple = (50, 75)
        self.__rect: pygame.Rect = pygame.Rect(self.__pos[0], self.__pos[1], 96*SCALE_OF_MONSTERS_IN_CLICKER, 96*SCALE_OF_MONSTERS_IN_CLICKER, border_radius=5)
        self.__health: float = MONSTER_HP_IN_CLICKER  # Здоровье монстра
        self.__monster_name: str = None
        self.__filename_of_sprite: str = None
        self.__sprite: SpriteSheet = None
        self.__frame_index: int = 0
        self.__state: str = "idle"
        self.__last_frame_tick: int = pygame.time.get_ticks()
        self.__cooldown: int = 200
        self.__monster_sprite_data: dict = {}

        self.change_monster()

    def display(self):
        a = self._get_frame_index()
        b = self._get_number_of_frames()
        if self.__state == "hurt":
            print('hurt')
        if self._get_frame_index() >= self._get_number_of_frames() - 1 and self._get_state != "idle":
            self.__state = "idle"
            self.__frame_index = 0
            self.set_cooldown(200)
            self.change_monster(self.__monster_name)
        if self._can_change_sprite():
            self.change_frame_index()

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Health: {self.__health}", True, BLACK)
        self.__screen.blit(self.__sprite.parse_sprite(scale=SCALE_OF_MONSTERS_IN_CLICKER, sprite_index=self.__frame_index, state=self.__state), (0, 0))

        self.__screen.blit(text_surface, (self.__rect.centerx, self.__rect.bottom + 10))

    def click_action(self):
        self.__state = 'hurt'
        self.__frame_index = 0
        self.change_monster(self.__monster_name)
        #self.set_cooldown(100)
        if self.__health <= 1:
            self.change_monster()
            self.__state = 'idle'
            self.__health = MONSTER_HP_IN_CLICKER
        else:
            self.change_hp_to_monster(-1)

    def change_monster(self, monster_name: str = None):
        self.__monster_name = random.choice(MONSTERS_IN_CLICKER) if monster_name is None else monster_name
        self.__filename_of_sprite = self.__monster_name + f"_sheet_{self.__state}.png"
        self.__sprite = SpriteSheet(self.__filename_of_sprite)
        self.__monster_sprite_data = self.__sprite.get_data()

    def change_monster_state(self, state):
        """
        Функция изменяет состояние текущего монстра, например монстр атакует или получает урон
        :param state:
        :return:
        """
        self.__state = state

    def set_hp_to_monster(self, value: float):
        self.health = value

    def change_hp_to_monster(self, value: float):
        self.__health += value

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def change_frame_index(self):
        self.__frame_index = (self.__frame_index + 1) % (self._get_number_of_frames())

    def set_cooldown(self, value: int):
        """
        Устанавливает задержку в смене кадров анимации спрайта
        :param value: значение в мс, через какое время должна произойти смена кадра анимации спрайта
        """

        self.__cooldown = value

    def _can_change_sprite(self) -> bool:
        """
        Функция проверяет прошло ли достаточно времени для смены кадра спрайта
        :return: True/False
        """
        now = pygame.time.get_ticks()
        if now - self.__last_frame_tick >= self.__cooldown:
            self.__last_frame_tick = now
            return True
        else:
            return False

    def _get_state(self) -> str:
        return self.__state

    def _get_number_of_frames(self) -> int:
        return self.__monster_sprite_data[self.__state]["info"]["numbers_of_frames"]

    def _get_frame_index(self) -> int:
        return self.__frame_index
# </editor-fold>


class Player:
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
