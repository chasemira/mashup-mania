import pygame

def player_b_selector(screen, quit_callback):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_callback()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "PlayerBChoice"  # Replace with actual selection
                if event.key == pygame.K_ESCAPE:
                    return None  # Go back to main menu
        screen.fill((30, 30, 90))
        # Optionally, draw instructions
        pygame.display.update()
    return None