__author__ = "Al0n1"
__version__ = "0.0.3"

from config import *
from colours import *
from spritesheet import SpriteSheet
import pygame
import random
import json


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

# <editor-fold desc="Классы меню">


class Menu:
    def __init__(self, screen, player_interface):
        self.__screen = screen
        self.__menu_items: list = []
        self.__running: bool = True
        self.__next_menu = None
        self.__prev_menu = None
        self.__interface = player_interface
        self.__background_color: tuple = WHITE
        self.__player = None

    def add_item(self, item: Button):
        self.__menu_items.append(item)

    def get_menu_items(self) -> list:
        return self.__menu_items

    def get_screen(self):
        return self.__screen

    def display_menu_items(self):
        for item in self.__menu_items:
            item.display()

    def handle_click(self, pos):
        for item in self.__menu_items:
            if item.get_rect().collidepoint(pos):
                item.click_action()

    def get_status(self) -> bool:
        return self.__running

    def change_status(self, status: bool = None):
        self.__running = not self.__running if status is None else status

    def initialize_buttons(self):
        pass

    def set_next_menu(self, menu):
        self.__next_menu = menu

    def set_prev_menu(self, menu):
        self.__prev_menu = menu
        menu.set_next_menu(self)

    def get_next_menu(self):
        return self.__next_menu

    def get_prev_menu(self):
        return self.__prev_menu

    def get_interface(self):
        return self.__interface

    def get_background_color(self):
        return self.__background_color

    def set_background_color(self, color):
        self.__background_color = color


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


class MainMenu(Menu):
    def __init__(self, screen, player_interface):
        super().__init__(screen, player_interface)

        self.initialize_buttons()

    def initialize_buttons(self):
        button1_x = (SCREEN_WIDTH - MAIN_MENU_BUTTON_WIDTH) // 2
        button1_y = (SCREEN_HEIGHT - MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

        button2_x = button1_x
        button2_y = button1_y + MAIN_MENU_BUTTON_HEIGHT + 30

        # Инициализация кнопки "Начать игру"
        StartButton(self, self.get_screen(),
                    pygame.Rect(button1_x, button1_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                    "Начать игру",
                    (0, 0, 0),
                    name="start",
                    font=pygame.font.SysFont(None, 48))

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pygame.Rect(button2_x, button2_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=pygame.font.SysFont(None, 48))


class ClickerMenu(Menu):
    def __init__(self, screen, main_menu, player_interface):
        super().__init__(screen, player_interface)

        self.__upgrades: list['UpgradeButton'] = []

        self.set_prev_menu(main_menu)
        self.initialize_items()
        self.__background_color: tuple = GRAY

    def initialize_items(self):
        exit_button_x, exit_button_y = SCREEN_WIDTH * .79, SCREEN_HEIGHT * .90

        # Инициализация кнопки "Выход"
        ExitButton(self, self.get_screen(),
                   pygame.Rect(exit_button_x, exit_button_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                   "Выход",
                   (0, 0, 0),
                   name="end",
                   font=BASIC_FONT)

        upgrade_button_y = CLICKER_UPGRADE_BUTTON_Y

        with open("upgrades.json", "r") as file:
            data = json.load(file)

        for upgrade in data.keys():
            if data[upgrade]["status"]:
                upgrade_button = UpgradeButton(menu=self, screen=self.get_screen(),
                                               rect=pygame.Rect(CLICKER_UPGRADE_BUTTON_X, upgrade_button_y,
                                                                CLICKER_UPGRADE_BUTTON_WIDTH,
                                                                CLICKER_UPGRADE_BUTTON_HEIGHT),
                                               text=data[upgrade]["text"].encode('windows-1251'),
                                               color=GRAY,
                                               name=upgrade,
                                               font=BASIC_FONT,
                                               target=data[upgrade]["target"],
                                               value=data[upgrade]["value"],
                                               status=data[upgrade]["status"])
            else:
                upgrade_button = UpgradeButton(menu=self, screen=self.get_screen(),
                                               rect=pygame.Rect(CLICKER_UPGRADE_BUTTON_X, upgrade_button_y,
                                                                CLICKER_UPGRADE_BUTTON_WIDTH,
                                                                CLICKER_UPGRADE_BUTTON_HEIGHT),
                                               text=data[upgrade]["text"].encode('windows-1251'),
                                               color=BLACK,
                                               name=upgrade,
                                               font=BASIC_FONT,
                                               target=data[upgrade]["target"],
                                               value=data[upgrade]["value"],
                                               status=data[upgrade]["status"])
            self.__upgrades.append(upgrade_button)
            upgrade_button_y += CLICKER_UPGRADE_BUTTON_INDENT + CLICKER_UPGRADE_BUTTON_HEIGHT

        self.add_item(Monster(screen=self.get_screen(), menu=self))
        self.__player = Player()

    def get_player(self) -> 'Player':
        return self.__player


class AutoClickerMenu:
    def display_menu(self):
        pass

    def handle_click(self):
        pass


# </editor-fold>


# <editor-fold desc="Классы монстров">
class Monster:
    """
    Класс для отображения монстра
    """

    def __init__(self, screen, menu):
        self.__screen: pygame.Surface = screen
        self.__pos: tuple = (50, 75)
        self.__rect: pygame.Rect = pygame.Rect(self.__pos[0], self.__pos[1], 96 * SCALE_OF_MONSTERS_IN_CLICKER,
                                               96 * SCALE_OF_MONSTERS_IN_CLICKER, border_radius=5)
        self.__health: float = MONSTER_HP_IN_CLICKER  # Здоровье монстра
        self.__monster_name: str = None
        self.__filename_of_sprite: str = None
        self.__sprite: SpriteSheet = None
        self.__frame_index: int = 0
        self.__state: str = "idle"
        self.__last_frame_tick: int = pygame.time.get_ticks()
        self.__cooldown: int = 200
        self.__monster_sprite_data: dict = {}
        self.__already_dead: bool = False  # метка того, что анимация смерти уже проигрывается, если true,то клики перестают обрабатываться
        self.__menu = menu

        self.__monster_window: pygame.Surface = pygame.Surface(
            (96 * SCALE_OF_MONSTERS_IN_CLICKER, 96 * SCALE_OF_MONSTERS_IN_CLICKER))

        self.change_monster()

    def display(self):
        if (self._get_frame_index() >= self._get_number_of_frames() - 1) and (self._get_state() != "idle"):
            if self.__state == 'dead':
                self.set_cooldown(500)
                if self._can_change_sprite():
                    self.__frame_index = 0
                    self.__state = "idle"
                    self.change_monster()
                    self.__health = MONSTER_HP_IN_CLICKER
                    self.__already_dead = False
                    self.set_cooldown(200)
            else:
                self.__frame_index = 0
                self.__state = "idle"
                self.change_monster(self.__monster_name)
        elif self._can_change_sprite():
            self.set_cooldown(200)
            self.change_frame_index()

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Health: {self.__health}", True, BLACK)
        self.__screen.blit(
            self.__sprite.parse_sprite(scale=SCALE_OF_MONSTERS_IN_CLICKER, sprite_index=self.__frame_index,
                                       state=self.__state, pos=self.__pos), (100, 0))

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




    def change_monster(self, monster_name: str = None):
        self.__monster_name = random.choice(MONSTERS_IN_CLICKER) if monster_name is None else monster_name
        self.__filename_of_sprite = self.__monster_name + f"_sheet_{self.__state}.png"
        self.__sprite = SpriteSheet(self.__filename_of_sprite)
        self.__monster_sprite_data = self.__sprite.get_data()

    def change_monster_state(self, state):
        """
        Функция изменяет состояние текущего монстра, например монстр атакует или получает урон
        :param state:
        :return:
        """
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
        """
        Устанавливает задержку в смене кадров анимации спрайта
        :param value: значение в мс, через какое время должна произойти смена кадра анимации спрайта
        """

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


# </editor-fold>


class Player:
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
        self.__clicker_damage: float = 1.

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

    def add_clicker_upgrades(self, upgrade: UpgradeButton):
        self.__clicker_upgrades.append(upgrade)

    def get_clicker_upgrades(self) -> list:
        return self.__clicker_upgrades
