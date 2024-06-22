__author__ = "Al0n1"
__version__ = "0.0.2"


import pygame as pg

from config import Utils


class AutoClicker:
    def __init__(self, menu, state: bool):
        self.__last_frame_tick: int = pg.time.get_ticks()
        self.__menu = menu

        self.__monster = self.__menu.get_monster()
        self.__player = self.__menu.get_player()

        self.__state = state

        self.__total_damage: float = self.calculate_damage()

    def do_click(self):
        if self._can_do_click():
            self.__monster.click_action(mode="auto")

    def _can_do_click(self) -> bool:
        now = pg.time.get_ticks()
        if self.__state and now - self.__last_frame_tick >= Utils.AUTO_CLICKER_COOLDOWN and self.__total_damage > 0:
            self.__last_frame_tick = now
            return True
        else:
            return False

    def get_state(self) -> bool:
        return self.__state

    def change_state(self):
        self.__state = not self.__state

    def increase_damage(self, damage: float):
        self.__total_damage += damage

    def parse_active_upgrades(self) -> list:
        all_upgrades = self.__menu.get_auto_upgrades_menu().get_upgrades()
        active_upgrades = []
        for upgrade in all_upgrades:
            if upgrade.get_status():
                active_upgrades.append(upgrade)
        return active_upgrades

    def calculate_damage(self) -> float:
        total_damage: float = 0
        upgrades = self.parse_active_upgrades()
        for upgrade in upgrades:
            total_damage += upgrade.get_value()

        return total_damage

    def update_damage(self):
        self.__total_damage = self.calculate_damage()

    def get_damage(self) -> float:
        return self.__total_damage
