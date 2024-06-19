__author__ = "Al0n1"
__version__ = "0.0.1"


import json
import pygame as pg

from config import Utils
from buttons import UpgradeButton
from colors import *


class ClickerUpgradesButtonMenu:
    def __init__(self, menu, mode: str, state: bool = False):
        self.__rect = pg.Rect(Utils.UPGRADE_MENU_X,
                              Utils.UPGRADE_MENU_Y,
                              Utils.UPGRADE_MENU_WIDTH,
                              Utils.UPGRADE_MENU_HEIGHT)
        self.__menu = menu

        self.__state: bool = state
        self.__mode = mode
        self.__upgrades: list[UpgradeButton] = []

        self._initialize_upgrades()

    def _initialize_upgrades(self):
        upgrade_button_y = Utils.CLICKER_UPGRADE_BUTTON_Y

        with open("upgrades.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        data = data[self.__mode]

        for upgrade in data.keys():
            upgrade_button = UpgradeButton(menu=self.__menu, screen=self.__menu.get_screen(),
                                           rect=pg.Rect(Utils.CLICKER_UPGRADE_BUTTON_X,
                                                        upgrade_button_y,
                                                        Utils.CLICKER_UPGRADE_BUTTON_WIDTH,
                                                        Utils.CLICKER_UPGRADE_BUTTON_HEIGHT),
                                           text=data[upgrade]["text"],
                                           color=GRAY if data[upgrade]["status"] else BLACK,
                                           name=upgrade,
                                           font=Utils.BASIC_FONT,
                                           target=data[upgrade]["target"],
                                           value=data[upgrade]["value"],
                                           status=data[upgrade]["status"],
                                           price=data[upgrade]["price"],
                                           mode=self.__mode,
                                           state=True)
            self.__upgrades.append(upgrade_button)
            upgrade_button_y += Utils.CLICKER_UPGRADE_BUTTON_INDENT + Utils.CLICKER_UPGRADE_BUTTON_HEIGHT

    def get_state(self) -> bool:
        return self.__state

    def display(self):
        for upgrade in self.__upgrades:
            upgrade.display()

    def get_upgrades(self) -> list:
        return self.__upgrades

    def click_action(self, pos):
        for upgrade in self.__upgrades:
            if upgrade.get_state() and not upgrade.get_status():
                if upgrade.get_rect().collidepoint(pos):
                    upgrade.click_action()

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def change_state(self):
        self.__state = not self.__state
