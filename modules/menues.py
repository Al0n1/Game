__author__ = "Al0n1"
__version__ = "0.0.1"


from colors import *
from config import Settings, Utils
from buttons import StartButton, ExitButton, UpgradeButton
import json
from enities import Monster, Player
import pygame


class Menu:
    def __init__(self, screen, player_interface):
        self.__screen = screen
        self.__menu_items: list = []
        self.__running: bool = True
        self.__next_menu = None
        self.__prev_menu = None
        self.__interface = player_interface
        self.__background_color: tuple = WHITE
        self.__player = None

    def add_item(self, item: object):
        self.__menu_items.append(item)

    def get_menu_items(self) -> list:
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


class MainMenu(Menu):
    def __init__(self, screen, player_interface):
        super().__init__(screen, player_interface)

        self.initialize_buttons()

    def initialize_buttons(self):
        button1_x = (Settings.SCREEN_WIDTH - Utils.MAIN_MENU_BUTTON_WIDTH) // 2
        button1_y = (Settings.SCREEN_HEIGHT - Utils.MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

        button2_x = button1_x
        button2_y = button1_y + Utils.MAIN_MENU_BUTTON_HEIGHT + 30

        # Инициализация кнопки "Начать игру"
        StartButton(self, self.get_screen(),
                    pygame.Rect(button1_x, button1_y, Utils.MAIN_MENU_BUTTON_WIDTH, Utils.MAIN_MENU_BUTTON_HEIGHT),
                    "Начать игру",
                    (0, 0, 0),
                    name="start",
                    font=pygame.font.SysFont(None, 48))

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pygame.Rect(button2_x, button2_y, Utils.MAIN_MENU_BUTTON_WIDTH, Utils.MAIN_MENU_BUTTON_HEIGHT),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=pygame.font.SysFont(None, 48))


class ClickerMenu(Menu):
    def __init__(self, screen, main_menu, player_interface):
        super().__init__(screen, player_interface)

        self.__upgrades: list['UpgradeButton'] = []

        self.set_prev_menu(main_menu)
        self.initialize_items()
        self.__background_color: tuple = GRAY

    def initialize_items(self):
        exit_button_x, exit_button_y = Settings.SCREEN_WIDTH * .79, Settings.SCREEN_HEIGHT * .90

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pygame.Rect(exit_button_x, exit_button_y, Utils.MAIN_MENU_BUTTON_WIDTH, Utils.MAIN_MENU_BUTTON_HEIGHT),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=Utils.BASIC_FONT)

        upgrade_button_y = Utils.CLICKER_UPGRADE_BUTTON_Y

        with open("upgrades.json", "r") as file:
            data = json.load(file)

        for upgrade in data.keys():
            upgrade_button = UpgradeButton(menu=self, screen=self.get_screen(),
                                           rect=pygame.Rect(Utils.CLICKER_UPGRADE_BUTTON_X, upgrade_button_y,
                                                            Utils.CLICKER_UPGRADE_BUTTON_WIDTH,
                                                            Utils.CLICKER_UPGRADE_BUTTON_HEIGHT),
                                           text=data[upgrade]["text"].encode('windows-1251'),
                                           color=GRAY if data[upgrade]["status"] else BLACK,
                                           name=upgrade,
                                           font=Utils.BASIC_FONT,
                                           target=data[upgrade]["target"],
                                           value=data[upgrade]["value"],
                                           status=data[upgrade]["status"])
            self.__upgrades.append(upgrade_button)
            upgrade_button_y += Utils.CLICKER_UPGRADE_BUTTON_INDENT + Utils.CLICKER_UPGRADE_BUTTON_HEIGHT

        self.add_item(Monster(screen=self.get_screen(), menu=self))
        self.__player = Player()

    def get_player(self) -> 'Player':
        return self.__player


class AutoClickerMenu:
    def display_menu(self):
        pass

    def handle_click(self):
        pass
