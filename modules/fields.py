__author__ = "Al0n1"
__version__ = "0.0.1"


from colors import *
from config import Utils
import pygame as pg


class Field:
    def __init__(self, menu, state: bool):
        self.__rect = None
        self.__menu = menu
        self.__state = state

    def display(self):
        pass

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def set_rect(self, rect):
        self.__rect = rect

    def click_action(self):
        pass

    def get_menu(self):
        return self.__menu

    def get_state(self) -> bool:
        return self.__state

    def change_state(self):
        self.__state = not self.__state

class MonsterHP(Field):
    def __init__(self, menu, state: bool = False):
        super().__init__(menu, state)

        menu = self.get_menu()
        self.__monster = menu.get_monster()
        self.__screen = menu.get_screen()

        self.__monster_rect: pg.Rect = self.__monster.get_rect()
        self.set_rect(pg.Rect(self.__monster_rect.centerx,
                              self.__monster_rect.bottom,
                              Utils.MONSTER_HP_WIDTH,
                              Utils.MONSTER_HP_HEIGHT)
                      )

    def display(self):
        health = self.__monster.get_hp()
        text_surface = Utils.BASIC_FONT.render(f"Health: {health}", True, BLACK)

        self.__screen.blit(text_surface, (self.get_rect().centerx, self.get_rect().bottom))


class PlayerMoney(Field):
    def __init__(self, menu, state: bool = False):
        super().__init__(menu, state)

        menu = self.get_menu()
        self.__monster = menu.get_monster()
        self.__screen = menu.get_screen()
        self.__player = menu.get_player()

        self.__monster_rect: pg.Rect = self.__monster.get_rect()
        self.set_rect(pg.Rect(self.__monster_rect.centerx,
                              self.__monster_rect.top,
                              Utils.PLAYER_MONEY_WIDTH,
                              Utils.PLAYER_MONEY_HEIGHT)
                      )

    def display(self):
        money = self.__player.get_money()
        text_surface = Utils.BASIC_FONT.render(f"Money: {money}", True, BLACK)

        self.__screen.blit(text_surface, (self.get_rect().right, self.get_rect().top))

    def input(self):
        pass


class PlayerDamage(Field):
    def __init__(self, menu, state: bool = False):
        super().__init__(menu, state)

        menu = self.get_menu()
        self.__monster = menu.get_monster()
        self.__screen = menu.get_screen()
        self.__player = menu.get_player()

        self.__monster_rect: pg.Rect = self.__monster.get_rect()
        self.set_rect(pg.Rect(self.__monster_rect.centerx,
                              self.__monster_rect.top,
                              Utils.PLAYER_DAMAGE_WIDTH,
                              Utils.PLAYER_DAMAGE_HEIGHT)
                      )

    def display(self):
        damage = self.__player.get_clicker_damage()
        text_surface = Utils.BASIC_FONT.render(f"Damage per click: {damage}", True, BLACK)

        self.__screen.blit(text_surface, (self.get_rect().right, self.get_rect().top + Utils.PLAYER_MONEY_DAMAGE_INDENT))


# class InputPlayerName:
