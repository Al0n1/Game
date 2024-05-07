import pygame


class MenuItem:
    def __init__(self, screen: pygame.display, rect: pygame.Rect, text: str, color: tuple, name: str = "name"):
        self.screen = screen
        self.rect = rect  # прямоугольник, описывающий положение и размер элемента
        self.text = text  # текст элемента
        self.color = color  # цвет текста
        self.name = name

    def display(self):
        # Отображение элемента на экране
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, border_radius=5)  # пример отображения элемента как прямоугольника
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def click_action(self):
        # Действие, выполняемое при клике на элемент
        if self.name == 'start':
            #return ClickerMenu(self)
            print("Start!")
        elif self.name == 'end':
            print("end")
            pygame.quit()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_items: MenuItem = []

    def display_menu(self):
        for item in self.menu_items:
            item.display()

    def handle_click(self, pos):
        for item in self.menu_items:
            if item.rect.collidepoint(pos):
                item.click_action()


"""class UpgradeButton:
    def __init__(self, screen, x, y, width, height, color, text, click_action):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.click_action = click_action

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

    def handle_click(self):
        self.click_action()"""


class ClickerMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        # Создание кнопок для улучшения кликов
        self.click_upgrade_buttons = []
        self.create_click_upgrade_buttons()

    def create_click_upgrade_buttons(self):
        # Создание кнопок для улучшения кликов
        button1 = ClickUpgradeButton(self.screen, 50, 100, 200, 50, (0, 0, 255), "Увеличить урон", self.increase_damage)
        button2 = ClickUpgradeButton(self.screen, 50, 200, 200, 50, (0, 0, 255), "Увеличить скорость клика", self.increase_click_speed)
        self.click_upgrade_buttons.extend([button1, button2])

    def increase_damage(self):
        # Реализация увеличения урона при клике
        pass

    def increase_click_speed(self):
        # Реализация увеличения скорости клика
        pass

    def draw(self):
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
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class Monster(Menu):
    def display_menu(self):
        pass

    def handle_click(self):
        pass


class Player:
    def __init__(self):
        self.__money: int = 10
        self.__player_items: list = []
        self.__clicker_upgrades: list = []
        self.__health: float = 100.0
