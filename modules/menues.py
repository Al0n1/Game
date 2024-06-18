__author__ = "Al0n1"
__version__ = "0.0.3"


import json
import pygame

from colors import *
from config import Settings, Utils
from buttons import StartButton, ExitButton, UpgradeButton
from player import Player
from fields import MonsterHP, PlayerMoney, PlayerDamage


class Menu:
    def __init__(self, screen, player_interface, game):
        self.__screen = screen
        self.__menu_items: list = []
        self.__running: bool = True
        self.__next_menu = None
        self.__prev_menu = None
        self.__interface = player_interface
        self.__background_color: tuple = WHITE
        self.__game = game

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

    def get_game(self) -> 'Game':
        return self.__game


class MainMenu(Menu):
    def __init__(self, screen, player_interface, game):
        super().__init__(screen, player_interface, game)

        self.initialize_items()

        """self.input_rect = pygame.Rect(200, 200, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False"""

    def initialize_items(self):
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

    """def get_status_of_input(self) -> bool:
        return self.active

    def change_status_of_input(self):
        self.active = not self.active

    def get_input_rect(self):
        return self.input_rect

    def change_color_of_input(self):
        self.color = self.color_active if self.color is self.color_passive else self.color_passive"""


class ClickerMenu(Menu):
    def __init__(self, screen, main_menu, player_interface, game):
        super().__init__(screen, player_interface, game)

        self.__upgrades: list['UpgradeButton'] = []

        self.__player = game.get_player()
        self.__monster = game.get_monster()

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

        with open("upgrades.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        for upgrade in data.keys():
            upgrade_button = UpgradeButton(menu=self, screen=self.get_screen(),
                                           rect=pygame.Rect(Utils.CLICKER_UPGRADE_BUTTON_X, upgrade_button_y,
                                                            Utils.CLICKER_UPGRADE_BUTTON_WIDTH,
                                                            Utils.CLICKER_UPGRADE_BUTTON_HEIGHT),
                                           text=data[upgrade]["text"],
                                           color=GRAY if data[upgrade]["status"] else BLACK,
                                           name=upgrade,
                                           font=Utils.BASIC_FONT,
                                           target=data[upgrade]["target"],
                                           value=data[upgrade]["value"],
                                           status=data[upgrade]["status"],
                                           price=data[upgrade]["price"])
            self.__upgrades.append(upgrade_button)
            upgrade_button_y += Utils.CLICKER_UPGRADE_BUTTON_INDENT + Utils.CLICKER_UPGRADE_BUTTON_HEIGHT

        self.add_item(self.__monster)

        self.add_item(MonsterHP(self))
        self.add_item(PlayerMoney(self))
        self.add_item(PlayerDamage(self))

    def get_player(self) -> 'Player':
        return self.__player

    def get_monster(self) -> 'Monster':
        return self.__monster

    def set_monster(self, monster: 'Monster'):
        self.__monster = monster

    def get_upgrades(self) -> list:
        return self.__upgrades


class ClickerUpgradesMenu:
    def __init__(self, menu):
        self.__menu = menu

        self.__upgrade = list

    def get_upgrades_from_file(self):
        upgrades = list

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
            upgrades.append(upgrade_button)

        return upgrades


class AutoClickerUpgradesMenu:
    def __init__(self, screen, player_interface, game):

        self.__monster = self.get_game().get_monster()

        self.__upgrades: list['UpgradeButton'] = []

        self.initialize_items()
        self.__background_color: tuple = GRAY

    def initialize_items(self):
        go_back_button_x, go_back_button_y = Settings.SCREEN_WIDTH * .79, Settings.SCREEN_HEIGHT * .90

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

        self.add_item(self.get_monster())

    def display(self):
        pass

