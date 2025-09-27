import pygame
from assets.menu.button import Button

BG = pygame.image.load("assets/menu/Background.png")

def get_font(size):
    return pygame.font.Font("assets/menu/font.ttf", size)

def main_menu(screen, play_callback, quit_callback):
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MASHUP MANIA", True, "#2761ae")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 250))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(640, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_callback()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_callback(screen)
                    return
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit_callback()
        pygame.display.update()