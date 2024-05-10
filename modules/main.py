"""
author: Al0n1
version: 0.0.1

:description:
Модуль для запуска игры
"""


from game import *
from config import *
from colours import *
from spritesheet import SpriteSheet
import pygame


def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player_interface = PlayerInterface()
    main_menu = MainMenu(screen, player_interface)
    clicker_menu = ClickerMenu(screen, main_menu, player_interface)

    menus = {
        "main menu": main_menu,
        "clicker menu": clicker_menu,
        #"rogue menu": RogueLikeMenu(screen),
        #"settings menu": SettingsMenu(screen)
    }
    menus["main menu"].set_background_color(LIGHT_GRAY)

    player_interface.set_menus(menus)
    player_interface.switch_menu("main menu")

    running = True
    while running:
        current_menu: 'Menu' = player_interface.get_current_menu()
        screen.fill(current_menu.get_background_color())
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
        clock.tick(60)


game()
