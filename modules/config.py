import pygame as pg
pg.init()


class Settings:
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 800


class Utils:
    # <editor-fold desc="Параметры главного меню">
    START_BUTTON_WIDTH: int = Settings.SCREEN_WIDTH * 3 // 10
    START_BUTTON_HEIGHT: int = Settings.SCREEN_HEIGHT // 10
    START_BUTTON_X: int = (Settings.SCREEN_WIDTH - START_BUTTON_WIDTH) // 2
    START_BUTTON_Y: int = (Settings.SCREEN_HEIGHT - START_BUTTON_HEIGHT) // 2 - 50
    START_BUTTON_RECT: pg.Rect = pg.Rect(START_BUTTON_X,
                                         START_BUTTON_Y,
                                         START_BUTTON_WIDTH,
                                         START_BUTTON_HEIGHT)

    START_EXIT_BUTTONS_INDENT: int = 30

    EXIT_BUTTON_WIDTH: int = Settings.SCREEN_WIDTH * 3 // 10
    EXIT_BUTTON_HEIGHT: int = Settings.SCREEN_HEIGHT // 10
    EXIT_BUTTON_X: int = (Settings.SCREEN_WIDTH - EXIT_BUTTON_WIDTH) // 2
    EXIT_BUTTON_Y: int = START_BUTTON_Y + START_BUTTON_HEIGHT + START_EXIT_BUTTONS_INDENT
    EXIT_BUTTON_RECT: pg.Rect = pg.Rect(EXIT_BUTTON_X,
                                        EXIT_BUTTON_Y,
                                        EXIT_BUTTON_WIDTH,
                                        EXIT_BUTTON_HEIGHT)
    # </editor-fold>

    # <editor-fold desc="Параметры меню кликера">
    CLICKER_EXIT_BUTTON_WIDTH: int = 100
    CLICKER_EXIT_BUTTON_HEIGHT: int = 50
    CLICKER_EXIT_BUTTON_X: int = 1100
    CLICKER_EXIT_BUTTON_Y: int = 750
    CLICKER_EXIT_BUTTON_RECT: pg.Rect = pg.Rect(CLICKER_EXIT_BUTTON_X,
                                                CLICKER_EXIT_BUTTON_Y,
                                                CLICKER_EXIT_BUTTON_WIDTH,
                                                CLICKER_EXIT_BUTTON_HEIGHT)

    CLICKER_UPGRADE_BUTTON_WIDTH: int = 400
    CLICKER_UPGRADE_BUTTON_HEIGHT: int = 50
    CLICKER_UPGRADE_BUTTON_INDENT: int = 10
    CLICKER_UPGRADE_BUTTON_X: int = Settings.SCREEN_WIDTH - CLICKER_UPGRADE_BUTTON_INDENT * 2 - CLICKER_UPGRADE_BUTTON_WIDTH
    CLICKER_UPGRADE_BUTTON_Y: int = 2

    UPGRADE_MENU_X: int = 700
    UPGRADE_MENU_Y: int = 0
    UPGRADE_MENU_WIDTH = CLICKER_UPGRADE_BUTTON_WIDTH
    UPGRADE_MENU_HEIGHT: int = 700
    UPGRADE_MENU_RECT: pg.Rect = pg.Rect(UPGRADE_MENU_X,
                                         UPGRADE_MENU_Y,
                                         UPGRADE_MENU_WIDTH,
                                         UPGRADE_MENU_HEIGHT)

    CHANGE_UPGRADES_MENU_BUTTON_X: int = Settings.SCREEN_WIDTH - 200
    CHANGE_UPGRADES_MENU_BUTTON_Y: int = Settings.SCREEN_HEIGHT - 100
    CHANGE_UPGRADES_MENU_BUTTON_WIDTH: int = 100
    CHANGE_UPGRADES_MENU_BUTTON_HEIGHT: int = 50
    CHANGE_UPGRADES_MENU_BUTTON_RECT = pg.Rect(CHANGE_UPGRADES_MENU_BUTTON_X,
                                               CHANGE_UPGRADES_MENU_BUTTON_Y,
                                               CHANGE_UPGRADES_MENU_BUTTON_WIDTH,
                                               CHANGE_UPGRADES_MENU_BUTTON_HEIGHT)
    CHANGE_UPGRADES_MENU_BUTTON_MANUAL_TO_AUTO = "Авто-кликер"
    CHANGE_UPGRADES_MENU_BUTTON_AUTO_TO_MANUAL = "Классический-кликер"
    # </editor-fold>

    # <editor-fold desc="Параметры монстра">
    MONSTERS_IN_CLICKER: list[str] = [
        'zombieMale',
        'zombieFemale',
        'zombieWild',
    ]
    MONSTER_MAX_HP_IN_CLICKER: float = 10.0
    SCALE_OF_MONSTERS_IN_CLICKER: int = 5
    REWARD_FOR_KILL: int = 1

    MONSTER_BASE_WIDTH: int = 96
    MONSTER_BASE_HEIGHT: int = 96
    MONSTER_X: int = 50
    MONSTER_Y: int = 75
    MONSTER_RECT: pg.Rect = pg.Rect(MONSTER_X,
                                    MONSTER_Y,
                                    MONSTER_BASE_WIDTH * SCALE_OF_MONSTERS_IN_CLICKER,
                                    MONSTER_BASE_HEIGHT * SCALE_OF_MONSTERS_IN_CLICKER)


    # </editor-fold>

    # <editor-fold desc="Параметры полей">
    MONSTER_HP_WIDTH: int = 100
    MONSTER_HP_HEIGHT: int = 50

    PLAYER_MONEY_WIDTH: int = 100
    PLAYER_MONEY_HEIGHT: int = 50
    PLAYER_MONEY_DAMAGE_INDENT = 20
    PLAYER_DAMAGE_WIDTH: int = 100
    PLAYER_DAMAGE_HEIGHT: int = 50
    # </editor-fold>

    # <editor-fold desc="Другие параметры">
    AUTO_CLICKER_COOLDOWN = 1000

    BASIC_FONT = pg.font.SysFont(None, 24)

    PLAYER_AUTO_SAVE_FILE_PATH: str = "saves/auto_save.json"
    # </editor-fold>
