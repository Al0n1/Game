__author__ = "Al0n1"
__version__ = "0.1.6"


import pygame as pg
import json
import os.path

from config import Settings, Utils
from colors import *
from menues import MainMenu, ClickerMenu, Menu
from player import Player
from monster import Monster
from autoclicker import AutoClicker


def get_saved_data(file_name: str = "auto_save", key: str = None):
    if not os.path.exists(f"saves/{file_name}.json"):
        print(f"Файл {Utils.PLAYER_AUTO_SAVE_FILE_PATH} не существует.")
        return None

    with open(f"saves/{file_name}.json", 'r') as f:
        content = f.read()
        if not content:
            print(f"Файл {file_name} пуст.")
            return None
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            return None
    return data[key] if key else data


class PlayerInterface:
    def __init__(self, menus: dict):
        self.__current_menu = None
        self.__menus: dict = menus

    def switch_menu(self, menu: str | object = None):
        if isinstance(menu, str) and menu is not None:
            self.__current_menu = self.__menus[menu]
        elif isinstance(menu, object) and menu is not None:
            self.__current_menu = menu
        else:
            self.__current_menu = None

    def get_current_menu(self) -> Menu:
        return self.__current_menu

    def get_menu(self, name: str) -> object:
        return self.__menus[name]

    def set_menus(self, menus: dict):
        self.__menus = menus


class Game:
    def __init__(self):
        self.__current_menu = None
        self.__screen = pg.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.__clock = pg.time.Clock()

        self.__player_interface = PlayerInterface({})

        self.__player = Player()
        self.__monster = Monster(screen=self.__screen)

        self.load_save()

        main_menu = MainMenu(screen=self.__screen,
                             player_interface=self.__player_interface,
                             game=self)
        clicker_menu = ClickerMenu(screen=self.__screen,
                                   main_menu=main_menu,
                                   player_interface=self.__player_interface,
                                   game=self)

        self.__menus: dict = {
            "main menu": main_menu,
            "clicker menu": clicker_menu
        }

        clicker_menu.set_monster(self.__monster)
        self.__monster.set_menu(clicker_menu)

        self.__auto_clicker = AutoClicker(menu=clicker_menu,
                                          state=True if len(clicker_menu.get_auto_upgrades_menu().get_upgrades()) > 0
                                          else False)

    def run(self):
        pg.init()

        self.__menus["main menu"].set_background_color(LIGHT_GRAY)

        self.__player_interface.set_menus(self.__menus)
        self.__player_interface.switch_menu("main menu")

        running = True
        while running:
            current_menu: 'Menu' = self.__player_interface.get_current_menu()
            self.__screen.fill(current_menu.get_background_color())
            current_menu.display_menu_items()
            self.__auto_clicker.do_click()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                    break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Нажата левая кнопка мыши
                        current_menu.handle_click(event.pos)
            if not current_menu.get_status():
                self.save_data()
                break
            self.__clock.tick(60)

    def save_data(self, file_name: str = "auto_save"):
        data = dict({"player": {}, "monster": {}})
        data["player"]["name"] = self.__player.get_name()
        data["player"]['money'] = self.__player.get_money()
        data["player"]['player_items'] = self.__player.get_items()
        data["player"]['health'] = self.__player.get_health()
        data["player"]['clicker_damage'] = self.__player.get_clicker_damage()
        data["player"]["stage"] = self.__player.get_stage()

        data["monster"]["name"] = self.__monster.get_name()
        data["monster"]["counter"] = self.__monster.get_monster_counter()
        data["monster"]["health"] = self.__monster.get_hp()
        data["monster"]["reward"] = self.__monster.get_reward()

        os.makedirs('saves', exist_ok=True)
        with open(f'saves/{file_name}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_save(self):
        player_data = get_saved_data(key="player")
        if player_data:
            self.__player.set_stage(player_data["stage"])
            self.__player.set_name(player_data["name"])
            self.__player.set_player_items(player_data["player_items"])
            self.__player.set_clicker_damage(player_data["clicker_damage"])
            self.__player.set_health(player_data["health"])
            self.__player.set_money(player_data["money"])

            stage = player_data["stage"]
            while stage > 0:
                Utils.MONSTER_MAX_HP_IN_CLICKER += 5
                stage -= 1

        monster_data = get_saved_data(key="monster")
        if monster_data:
            self.__monster.set_name(monster_data["name"])
            self.__monster.set_monster_counter(monster_data["counter"])
            self.__monster.set_hp_to_monster(monster_data["health"])
            self.__monster.set_reward(monster_data["reward"])

    def get_player(self) -> Player:
        return self.__player

    def get_monster(self) -> Monster:
        return self.__monster

    def get_auto_clicker(self) -> AutoClicker:
        return self.__auto_clicker
