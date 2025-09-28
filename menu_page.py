import pygame
from assets.menu.button import Button

def get_font(size):
    return pygame.font.Font("assets/menu/font.ttf", size)

def main_menu(screen, play_callback, quit_callback):
    screen_width, screen_height = screen.get_size()
    
    # Load and scale background to fit screen
    BG = pygame.image.load("assets/menu/Background.png")
    BG = pygame.transform.scale(BG, (screen_width, screen_height))
    
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # Center the title text based on screen size
        MENU_TEXT = get_font(100).render("MASHUP MANIA", True, "#007bff")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, screen_height // 3))
        
        # Center buttons based on screen size
        PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), 
                            pos=(screen_width // 2, screen_height // 2),
                            text_input="PLAY", font=get_font(75), 
                            base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), 
                            pos=(screen_width // 2, screen_height // 2 + 150),
                            text_input="QUIT", font=get_font(75), 
                            base_color="#d7fcd4", hovering_color="White")
        
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