import pygame


class Settings:
    pygame.init()

    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 800


class Utils:
    MAIN_MENU_BUTTON_WIDTH: int = Settings.SCREEN_WIDTH * 3 // 10
    MAIN_MENU_BUTTON_HEIGHT: int = Settings.SCREEN_HEIGHT // 10

    CLICKER_MENU_BUTTON_WIDTH: int = Settings.SCREEN_WIDTH * 1.5 // 10
    CLICKER_MENU_BUTTON_HEIGHT: int = Settings.SCREEN_HEIGHT // 15

    CLICKER_UPGRADE_BUTTON_WIDTH: int = 400
    CLICKER_UPGRADE_BUTTON_HEIGHT: int = 50
    CLICKER_UPGRADE_BUTTON_INDENT: int = 10
    CLICKER_UPGRADE_BUTTON_X: int = Settings.SCREEN_WIDTH - CLICKER_UPGRADE_BUTTON_INDENT * 2 - CLICKER_UPGRADE_BUTTON_WIDTH
    CLICKER_UPGRADE_BUTTON_Y: int = 2

    MONSTERS_IN_CLICKER: list[str] = [
        'zombieMale',
        'zombieFemale',
        'zombieWild',
    ]
    MONSTER_HP_IN_CLICKER: float = 10.0
    SCALE_OF_MONSTERS_IN_CLICKER: int = 5

    BASIC_FONT = pygame.font.SysFont(None, 24)
