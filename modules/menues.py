__author__ = "Al0n1"
__version__ = "0.0.4"


import pygame as pg

from colors import *
from config import Settings, Utils
from buttons import StartButton, ExitButton, ChangeModeButton
from player import Player
from fields import MonsterHP, PlayerMoney, PlayerDamage
from upgrades import ClickerUpgradesButtonMenu
from monster import Monster


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
            if item.get_state():
                item.display()

    def handle_click(self, pos):
        for item in self.__menu_items:
            if item.get_state():
                if item.get_rect().collidepoint(pos):
                    if type(item) == ClickerUpgradesButtonMenu:
                        item.click_action(pos)
                    elif type(item) == Monster:
                        item.click_action(mode="manual")
                    else:
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

        """self.input_rect = pg.Rect(200, 200, 140, 32)
        self.color_active = pg.Color('lightskyblue3')
        self.color_passive = pg.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False"""

    def initialize_items(self):
        button1_x = (Settings.SCREEN_WIDTH - Utils.MAIN_MENU_BUTTON_WIDTH) // 2
        button1_y = (Settings.SCREEN_HEIGHT - Utils.MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

        button2_x = button1_x
        button2_y = button1_y + Utils.MAIN_MENU_BUTTON_HEIGHT + 30

        # Инициализация кнопки "Начать игру"
        StartButton(self, self.get_screen(),
                    pg.Rect(button1_x, button1_y, Utils.MAIN_MENU_BUTTON_WIDTH, Utils.MAIN_MENU_BUTTON_HEIGHT),
                    "Начать игру",
                    (0, 0, 0),
                    name="start",
                    font=pg.font.SysFont(None, 48),
                    state=True)

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pg.Rect(button2_x, button2_y, Utils.MAIN_MENU_BUTTON_WIDTH, Utils.MAIN_MENU_BUTTON_HEIGHT),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=pg.font.SysFont(None, 48),
                   state=True)

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

        self.__player = game.get_player()
        self.__monster = game.get_monster()

        self.set_prev_menu(main_menu)
        self.__background_color: tuple = GRAY

        self.__manual_upgrades_menu = ClickerUpgradesButtonMenu(menu=self, mode="manual", state=True)
        self.__auto_upgrades_menu = ClickerUpgradesButtonMenu(menu=self, mode="auto", state=False)

        self.initialize_items()

    def initialize_items(self):
        exit_button_x, exit_button_y = 1100, 750

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pg.Rect(exit_button_x, exit_button_y, 100, 50),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=Utils.BASIC_FONT,
                   state=True)

        ChangeModeButton(menu=self,
                         name="change_mode",
                         screen=self.get_screen(),
                         rect=Utils.CHANGE_UPGRADES_MENU_BUTTON_RECT,
                         text=Utils.CHANGE_UPGRADES_MENU_BUTTON_MANUAL_TO_AUTO,
                         color=BLACK,
                         state=True,
                         font=Utils.BASIC_FONT,
                         current_mode="manual")

        self.add_item(self.__monster)
        self.add_item(self.get_manual_upgrades_menu())
        self.add_item(self.get_auto_upgrades_menu())

        self.add_item(MonsterHP(menu=self, state=True))
        self.add_item(PlayerMoney(menu=self, state=True))
        self.add_item(PlayerDamage(menu=self, state=True))



    def get_player(self) -> 'Player':
        return self.__player

    def get_monster(self) -> 'Monster':
        return self.__monster

    def set_monster(self, monster: 'Monster'):
        self.__monster = monster

    def get_manual_upgrades_menu(self) -> ClickerUpgradesButtonMenu:
        return self.__manual_upgrades_menu

    def get_auto_upgrades_menu(self) -> ClickerUpgradesButtonMenu:
        return self.__auto_upgrades_menu
