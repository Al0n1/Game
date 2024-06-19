__author__ = "Al0n1"
__version__ = "0.0.5"


import pygame
import json

from colors import *
from config import Utils


class Button:
    def __init__(self, menu: 'Menu', screen, rect: pygame.Rect, text: str, color: tuple, name: str,
                 font: pygame.font.SysFont, state: bool):
        self.__screen = screen
        self.__rect = rect  # прямоугольник, описывающий положение и размер элемента
        self.__text = text  # текст элемента
        self.__color = color  # цвет текста
        self.__name = name
        self.__menu = menu
        self.__font = font
        self.__state: bool = state

    def change_state(self):
        self.__state = not self.__state

    def get_state(self) -> bool:
        return self.__state

    def click_action(self):
        pass

    def button_released(self):
        pass

    def assign_button_to_menu(self):
        self.__menu.add_item(self)

    def display(self):
        pygame.draw.rect(self.__screen, (255, 255, 255), self.__rect, border_radius=5)
        text_surface = self.__font.render(self.__text, True, self.__color)
        text_rect = text_surface.get_rect(center=self.__rect.center)
        self.__screen.blit(text_surface, text_rect)

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def get_menu(self) -> 'Menu':
        return self.__menu

    def get_text(self) -> str:
        return self.__text

    def get_name(self) -> str:
        return self.__name

    def set_color(self, color: tuple):
        self.__color = color

    def change_text(self, text: str):
        self.__text = text


class ExitButton(Button):
    def __init__(self, menu: 'Menu', screen, rect: pygame.Rect, text: str, color: tuple, name: str,
                 font: pygame.font.SysFont, state: bool = False):
        super().__init__(menu, screen, rect, text, color, name, font, state)
        if self.get_menu() is not None:
            self.assign_button_to_menu()

    def click_action(self):
        print("end")
        self.get_menu().change_status(False)
        pygame.quit()


class StartButton(Button):
    def __init__(self, menu: 'Menu', screen, rect: pygame.Rect, text: str, color: tuple, name: str,
                 font: pygame.font.SysFont, state: bool = False):
        super().__init__(menu, screen, rect, text, color, name, font, state)
        if self.get_menu() is not None:
            self.assign_button_to_menu()

    def click_action(self):
        print("Start!")
        interface = self.get_menu().get_interface()
        interface.switch_menu(self.get_menu().get_next_menu())


class UpgradeButton(Button):
    def __init__(self, name: str, target: object, value: float, text: str, menu: 'ClickerMenu', screen, rect: pygame.Rect,
                 color: tuple, font: pygame.font.SysFont, status: bool, price: int, mode: str, state: bool = False):
        super().__init__(menu, screen, rect, text, color, name, font, state)
        self.__target = target
        self.__value: float = value
        self.__status: bool = status
        self.__price: int = price
        self.change_text(self.get_text() + f" | {self.__price}")
        self.__mode: str = mode
        #self.__menu_state: bool = menu.get_state()

    def change_status(self):
        self.__status = not self.__status
        with open('upgrades.json', 'r') as f:
            data = json.load(f)
        data[self.__mode][self.get_name()]['status'] = not data[self.__mode][self.get_name()]['status']
        with open('upgrades.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def change_mode(self):
        self.__mode = "auto" if self.__mode == "manual" else "manual"

    def get_value(self) -> float:
        return self.__value

    def get_target(self):
        return self.__target

    def get_status(self) -> bool:
        return self.__status

    def get_price(self) -> int:
        return self.__price

    def click_action(self):
        value = self.get_value()
        target = self.get_target()
        price = self.get_price()
        if target == "clickerPlayer":
            if self.get_menu().get_player().get_money() >= price:
                self.change_status()
                self.get_menu().get_player().increase_player_damage(value)
                self.get_menu().get_player().change_money(-price)
                self.set_color(GRAY)
        if target == "clickerAuto":
            if self.get_menu().get_player().get_money() >= price:
                self.change_status()
                self.get_menu().get_player().change_money(-price)
                self.get_menu().get_game().get_auto_clicker().update_damage()
                self.set_color(GRAY)


class ChangeModeButton(Button):
    def __init__(self, name: str, text: str, menu: 'ClickerMenu', screen,
                 rect: pygame.Rect,
                 color: tuple, font: pygame.font.SysFont, current_mode: str, state: bool = False):
        super().__init__(menu, screen, rect, text, color, name, font, state)

        self.__current_mode: str = current_mode

        if self.get_menu() is not None:
            self.assign_button_to_menu()

    def change_menu(self):
        self.get_menu().get_manual_upgrades_menu().change_state()
        self.get_menu().get_auto_upgrades_menu().change_state()
        self.change_text(Utils.CHANGE_UPGRADES_MENU_BUTTON_AUTO_TO_MANUAL if self.__current_mode == "manual" else Utils.CHANGE_UPGRADES_MENU_BUTTON_MANUAL_TO_AUTO)
        self.change_current_mode()

    def change_current_mode(self):
        self.__current_mode = "auto" if self.__current_mode == "manual" else "manual"

    def click_action(self):
        self.change_menu()
