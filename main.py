import pygame
from game import *
from config import *
from colours import *


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
    player_interface.set_menus(menus)
    player_interface.switch_menu("main menu")
    monster = Monster(screen, 100, 100, 30, 30, RED)

    running = True
    while running:
        current_menu = player_interface.get_current_menu()
        screen.fill(LIGHT_GRAY)
        current_menu.display_menu_items()
        pygame.display.flip()
        monster.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    current_menu.handle_click(event.pos)
        if not current_menu.get_status():
            break
        clock.tick(60)


game()
