__author__ = "Al0n1"
__version__ = "0.0.2"

import pygame
from config import Utils
from spritesheet import SpriteSheet
from colors import *
import random
import json


class Monster:
    def __init__(self, screen, menu):
        self.__screen: pygame.Surface = screen
        self.__pos: tuple = (50, 75)
        self.__rect: pygame.Rect = pygame.Rect(self.__pos[0], self.__pos[1], 96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER,
                                               96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER)
        self.__health: float = Utils.MONSTER_HP_IN_CLICKER  # Здоровье монстра
        self.__monster_name: str = ""
        self.__filename_of_sprite: str = ""
        self.__sprite: SpriteSheet = None
        self.__frame_index: int = 0
        self.__state: str = "idle"
        self.__last_frame_tick: int = pygame.time.get_ticks()
        self.__cooldown: int = 200
        self.__monster_sprite_data: dict = {}
        self.__already_dead: bool = False  # метка того, что анимация смерти уже проигрывается, если true, то клики
        # перестают обрабатываться
        self.__menu = menu

        self.__monster_window: pygame.Surface = pygame.Surface(
            (96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER, 96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER))

        self.change_monster()

    def display(self):
        if (self._get_frame_index() >= self._get_number_of_frames() - 1) and (self._get_state() != "idle"):
            if self.__state == 'dead':
                self.set_cooldown(500)
                if self._can_change_sprite():
                    self.__frame_index = 0
                    self.__state = "idle"
                    self.change_monster()
                    self.__health = Utils.MONSTER_HP_IN_CLICKER
                    self.__already_dead = False
                    self.set_cooldown(200)
            else:
                self.__frame_index = 0
                self.__state = "idle"
                self.change_monster(self.__monster_name)
        elif self._can_change_sprite():
            self.set_cooldown(200)
            self.change_frame_index()

        text_surface = Utils.BASIC_FONT.render(f"Health: {self.__health}", True, BLACK)
        self.__screen.blit(
            self.__sprite.parse_sprite(scale=Utils.SCALE_OF_MONSTERS_IN_CLICKER, sprite_index=self.__frame_index,
                                       state=self.__state), (100, 0))

        self.__screen.blit(text_surface, (self.__rect.centerx, self.__rect.bottom + 10))

    def click_action(self):
        if not self.__already_dead:
            self.__state = 'hurt'
            self.__frame_index = 0
            self.change_monster(self.__monster_name)  # Переключает спрайт стоящего зомби на зомби получающего удар
            self.change_hp_to_monster(-self.__menu.get_player().get_clicker_damage())

            # Обработка смерти монстра
            if self.__health < 1:
                if self.__health < 0:
                    self.__health = 0
                self.__state = 'dead'
                self.change_monster(self.__monster_name)
                self.__already_dead = True
                self.__menu.get_player().change_money(Utils.REWARD_FOR_KILL)

    def change_monster(self, monster_name: str = None):
        self.__monster_name = random.choice(Utils.MONSTERS_IN_CLICKER) if monster_name is None else monster_name
        self.__filename_of_sprite = self.__monster_name + f"_sheet_{self.__state}.png"
        self.__sprite = SpriteSheet(self.__filename_of_sprite)
        self.__monster_sprite_data = self.__sprite.get_data()

    def change_monster_state(self, state):
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


class Player:
    def __init__(self, saved_data: dict = None):
        if saved_data is None:
            self.__name = "Player"
            self.__money: int = 10
            self.__player_items: list = []
            self.__health: float = 100.0
            self.__clicker_damage: float = 1.
        else:
            self.__name: str = saved_data["name"]
            self.__money: int = saved_data["money"]
            self.__player_items: list = saved_data["player_items"]
            self.__health: float = saved_data["health"]
            self.__clicker_damage: float = saved_data["clicker_damage"]

        self._initialize_upgrades()

    def _initialize_upgrades(self):
        with open("upgrades.json") as file:
            data = json.load(file)
        for upgrade in data.keys():
            if data[upgrade]["status"] and data[upgrade]["target"] == "clickerPlayer":
                self.__clicker_damage = data[upgrade]["value"]

    def change_clicker_damage(self, value: float):
        self.__clicker_damage = value

    def get_clicker_damage(self) -> float:
        return self.__clicker_damage

    def get_money(self) -> float:
        return self.__money

    def get_items(self) -> list:
        return self.__player_items

    def get_health(self) -> float:
        return self.__health

    def change_name(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def change_money(self, money: float):
        self.__money += money

    def set_name(self, name: str):
        self.__name = name
