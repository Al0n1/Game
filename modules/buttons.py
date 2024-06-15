__author__ = "Al0n1"
__version__ = "0.0.1"


import pygame
import json
from colors import *


class Button:
    def __init__(self, menu: 'Menu', screen, rect: pygame.Rect, text: str, color: tuple, name: str,
                 font: pygame.font.SysFont):
        self.__screen = screen
        self.__rect = rect  # прямоугольник, описывающий положение и размер элемента
        self.__text = text  # текст элемента
        self.__color = color  # цвет текста
        self.__name = name
        self.__menu = menu
        self.__font = font
        if self.__menu is not None:
            self.assign_button_to_menu()

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


class ExitButton(Button):
    def click_action(self):
        print("end")
        self.get_menu().change_status(False)
        pygame.quit()


class StartButton(Button):
    def click_action(self):
        print("Start!")
        interface = self.get_menu().get_interface()
        interface.switch_menu(self.get_menu().get_next_menu())


class UpgradeButton(Button):
    def __init__(self, name: str, target: object, value: float, text: str, menu: 'ClickerMenu', screen, rect: pygame.Rect,
                 color: tuple, font: pygame.font.SysFont, status: bool):
        super().__init__(menu, screen, rect, text, color, name, font)
        self.__target = target
        self.__value = value
        self.__status = status

    def change_status(self):
        self.__status = not self.__status
        with open('upgrades.json') as f:
            data = json.load(f)
        data[self.get_name()]['status'] = not data[self.get_name()]['status']
        with open('upgrades.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_value(self):
        return self.__value

    def get_target(self):
        return self.__target

    def get_status(self):
        return self.__status

    def click_action(self):
        if not self.__status:
            self.change_status()
            value = self.get_value()
            target = self.get_target()
            if target == "clickerPlayer":
                self.get_menu().get_player().change_clicker_damage(value)
            self.set_color(GRAY)
