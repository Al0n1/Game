__author__ = "Al0n1"
__version__ = "0.0.2"


import json


class Player:
    def __init__(self, saved_data: dict = None):
        if saved_data is None:
            self.__name = "Player"
            self.__money: int = 10
            self.__player_items: list = []
            self.__health: float = 100.0
            self.__clicker_damage: float = 1.
            self.__stage = 0
        else:
            self.__name: str = saved_data["name"]
            self.__money: int = saved_data["money"]
            self.__player_items: list = saved_data["player_items"]
            self.__health: float = saved_data["health"]
            self.__clicker_damage: float = saved_data["clicker_damage"]
            self.__stage: int = saved_data["stage"]

        self._initialize_upgrades()

    def _initialize_upgrades(self):
        with open("upgrades.json") as file:
            data = json.load(file)
        data = data["manual"]
        for upgrade in data.keys():
            if data[upgrade]["status"] and data[upgrade]["target"] == "clickerPlayer":
                self.__clicker_damage = data[upgrade]["value"]

    def set_clicker_damage(self, value: float):
        self.__clicker_damage = value

    def increase_player_damage(self, value: float):
        self.__clicker_damage += value

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

    def get_stage(self) -> int:
        return self.__stage

    def increment_stage(self):
        self.__stage += 1

    def set_stage(self, stage: int):
        self.__stage = stage

    def set_money(self, money: int):
        self.__money = money

    def set_player_items(self, items: list):
        self.__player_items = items

    def set_health(self, value: float):
        self.__health = value
