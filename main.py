import pygame
from game import *
from config import *
from colours import colours


def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    menus = {
        "main menu": MainMenu(screen),
        "clicker menu": ClickerMenu(screen),
        #"rogue menu": RogueLikeMenu(screen),
        #"settings menu": SettingsMenu(screen)
    }
    player_interface = PlayerInterface(menus)
    player_interface.switch_menu("main menu")

    running = True
    while running:
        current_menu = player_interface.get_current_menu()
        screen.fill(colours["light gray"])
        current_menu.display_menu()
        pygame.display.flip()

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
