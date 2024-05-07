"""
Модуль содержащий классы игры
"""

import pygame


class MenuItem:
    """
    Класс кнопок меню
    """
    def __init__(self, screen: pygame.display, rect: pygame.Rect, text: str, color: tuple, name: str = "name"):
        """

        :param screen:
        :param rect:
        :param text:
        :param color:
        :param name:
        """
        self.screen = screen
        self.rect = rect  # прямоугольник, описывающий положение и размер элемента
        self.text = text  # текст элемента
        self.color = color  # цвет текста
        self.name = name

    def display(self):
        """

        :return:
        """
        # Отображение элемента на экране
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, border_radius=5)  # пример отображения элемента как прямоугольника
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def click_action(self):
        """

        :return:
        """
        # Действие, выполняемое при клике на элемент
        if self.name == 'start':
            clicker_menu = ClickerMenu(self.screen)
            clicker_menu.run()
            print("Start!")
        elif self.name == 'end':
            print("end")
            pygame.quit()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_items: MenuItem = []

    def display_menu(self):
        pass

    def handle_click(self):
        pass


class MainMenu(Menu):
    """
    Класс меню
    """
    def display_menu(self):
        """

        :return:
        """
        for item in self.menu_items:
            item.display()

    def handle_click(self, pos):
        """

        :param pos:
        :return:
        """
        for item in self.menu_items:
            if item.rect.collidepoint(pos):
                item.click_action()


class UpgradeButton:
    """
    Класс кнопок в меню кликера
    """
    def __init__(self, screen, x, y, width, height, color, text, click_action):
        """

        :param screen:
        :param x:
        :param y:
        :param width:
        :param height:
        :param color:
        :param text:
        :param click_action:
        """
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.click_action = click_action

    def draw(self):
        """

        :return:
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

    def handle_click(self):
        """

        :return:
        """
        self.click_action()


class ClickerMenu(Menu):
    """
    Класс меню кликера
    """
    def __init__(self, screen):
        super().__init__(screen)

        # Создание кнопок для улучшения кликов
        self.click_upgrade_buttons = []
        self.create_click_upgrade_buttons()

    def create_click_upgrade_buttons(self):
        """

        :return:
        """
        # Создание кнопок для улучшения кликов
        button1 = UpgradeButton(self.screen, 50, 100, 200, 50, (0, 0, 255), "Увеличить урон", self.increase_damage)
        button2 = UpgradeButton(self.screen, 50, 200, 200, 50, (0, 0, 255), "Увеличить скорость клика", self.increase_click_speed)
        self.click_upgrade_buttons.extend([button1, button2])

    def increase_damage(self):
        """

        :return:
        """
        # Реализация увеличения урона при клике
        pass

    def increase_click_speed(self):
        """

        :return:
        """
        # Реализация увеличения скорости клика
        pass

    def draw(self):
        """

        :return:
        """
        # Отрисовка меню кликера
        super().draw()  # Отрисовка базового меню

        # Отрисовка кнопок для улучшения кликов
        for button in self.click_upgrade_buttons:
            button.draw()

    def handle_click(self, pos):
        # Обработка клика в меню кликера
        super().handle_click(pos)  # Обработка клика в базовом меню

        # Проверка клика по кнопкам для улучшения кликов
        for button in self.click_upgrade_buttons:
            if button.rect.collidepoint(pos):
                button.handle_click()


class AutoClickerMenu(Menu):
    """
    Класс меню прокачки автокликера
    """
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class Monster(Menu):
    """
    Класс монтсров
    """
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class Player:
    """
    Класс игрока
    """
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
