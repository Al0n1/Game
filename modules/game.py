__author__ = "Al0n1"
__version__ = "0.1.0"


from config import Settings
from colors import *
from menues import MainMenu, ClickerMenu, Menu

import pygame


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
        self.__screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.__clock = pygame.time.Clock()

        self.__player_interface = PlayerInterface({})

        main_menu = MainMenu(self.__screen, self.__player_interface)
        clicker_menu = ClickerMenu(self.__screen, main_menu, self.__player_interface)

        self.__menus: dict = {
            "main menu": main_menu,
            "clicker menu": clicker_menu,
            # "rogue menu": RogueLikeMenu(screen),
            # "settings menu": SettingsMenu(screen)
        }

    def run(self):
        pygame.init()

        self.__menus["main menu"].set_background_color(LIGHT_GRAY)

        self.__player_interface.set_menus(self.__menus)
        self.__player_interface.switch_menu("main menu")

        running = True
        while running:
            current_menu: 'Menu' = self.__player_interface.get_current_menu()
            self.__screen.fill(current_menu.get_background_color())
            current_menu.display_menu_items()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        current_menu.handle_click(event.pos)
            if not current_menu.get_status():
                break
            self.__clock.tick(60)
