"""
author: Al0n1
version: 0.0.2

:description:
Модуль констант
"""


SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
MAIN_MENU_BUTTON_WIDTH: int = SCREEN_WIDTH * 3 // 10
MAIN_MENU_BUTTON_HEIGHT: int = SCREEN_HEIGHT // 10
CLICKER_MENU_BUTTON_WIDTH: int = SCREEN_WIDTH * 1.5 // 10
CLICKER_MENU_BUTTON_HEIGHT: int = SCREEN_HEIGHT // 15

MONSTERS_IN_CLICKER: list[str] = [
    'zombieMale',
    'zombieFemale',
    'zombieWild',
]
SCALE_OF_MONSTERS_IN_CLICKER: int = 3
PLAYER_DAMAGE_IN_CLICKER: float = 1.0
MONSTER_HP_IN_CLICKER: float = 10.0
