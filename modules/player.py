__author__ = "Al0n1"
__version__ = "0.0.1"


import json


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