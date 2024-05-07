import pygame
from game import *
from config import *
from colours import colours


def start_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    menu = Menu(screen)

    button1_x = (SCREEN_WIDTH - MAIN_MENU_BUTTON_WIDTH) // 2
    button1_y = (SCREEN_HEIGHT - MAIN_MENU_BUTTON_HEIGHT) // 2 - 50

    button2_x = button1_x
    button2_y = button1_y + MAIN_MENU_BUTTON_HEIGHT + 30

    item1 = MenuItem(screen, pygame.Rect(button1_x, button1_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                     "Новая игра",
                     (0, 0, 0),
                     "start")
    item2 = MenuItem(screen, pygame.Rect(button2_x, button2_y, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT),
                     "Выход",
                     (0, 0, 0),
                     "end")

    menu.menu_items.extend([item1, item2])

    running = True
    while running:
        screen.fill(colours["light gray"])
        menu.display_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    menu.handle_click(event.pos)

        clock.tick(60)

    pygame.quit()


start_game()