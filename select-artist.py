import pygame, sys
from assets.menu.button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/menu/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)



def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("Player 1", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))




        SCREEN.blit(MENU_TEXT, MENU_RECT)



        pygame.display.update()

main_menu()