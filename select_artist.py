import pygame, sys, os, math
from assets.menu.button import Button
from backend import ARTIST_OPTIONS_A, ARTIST_OPTIONS_B

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BG = pygame.image.load(os.path.join(CURRENT_DIR, "assets", "menu", "Background.png"))

def get_font(size):
    return pygame.font.Font(os.path.join(CURRENT_DIR, "assets", "menu", "font.ttf"), size)

def load_artist_images(base_size):
    """Preload all artist images with scaling based on screen size"""
    images = {}
    image_mappings = {
        'Weeknd': 'weeknd.jpg',
        'Bruno': 'bruno.jpeg',
        'Rihanna': 'rihanna.webp',
        'Billie': 'billie.jpg',
        'Taylor': 'taylor.webp',
        'Arianna': 'arianna.webp',
        'Sabrina': 'sabrina.jpg',
        'Olivia': 'olivia.webp',
        'Malone': 'malone.jpg',
        'Michael': 'Michael.jpg'  
    }
    for artist, filename in image_mappings.items():
        try:
            path = os.path.join(CURRENT_DIR, "assets", "artist-img", filename)
            original = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.smoothscale(original, (base_size, base_size))
            images[artist] = scaled
        except pygame.error:
            surface = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
            pygame.draw.circle(surface, (100, 100, 100), (base_size//2, base_size//2), base_size//2 - 5)
            pygame.draw.circle(surface, (150, 150, 150), (base_size//2, base_size//2), base_size//2 - 5, 3)
            images[artist] = surface
    return images

class ArtistCircle:
    def __init__(self, pos, artist_name, radius, image):
        self.pos = pos
        self.artist_name = artist_name
        self.radius = radius
        self.selected = False
        self.hover = False
        self.pulse_offset = 0
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def update(self, mouse_pos):
        distance = math.hypot(mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        self.hover = distance <= self.radius
        if self.selected:
            self.pulse_offset = (self.pulse_offset + 0.15) % (2 * math.pi)

    def draw(self, screen, font_size):
        if self.selected:
            pulse_intensity = 0.7 + 0.3 * math.sin(self.pulse_offset)
            border_color = (int(0 * pulse_intensity), int(255 * pulse_intensity), int(100 * pulse_intensity))
            border_size = int(self.radius * 2.1)
            border_rect = pygame.Rect(0, 0, border_size, border_size)
            border_rect.center = self.pos
            for i in range(3):
                alpha = int(120 * pulse_intensity * (3-i) / 3)
                glow_size = border_size + i * 6
                glow_rect = pygame.Rect(0, 0, glow_size, glow_size)
                glow_rect.center = self.pos
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*border_color, alpha), glow_surf.get_rect(), border_radius=15)
                screen.blit(glow_surf, glow_rect)
            pygame.draw.rect(screen, border_color, border_rect, width=4, border_radius=12)
        elif self.hover:
            hover_size = int(self.radius * 2.05)
            hover_rect = pygame.Rect(0, 0, hover_size, hover_size)
            hover_rect.center = self.pos
            hover_surf = pygame.Surface((hover_size, hover_size), pygame.SRCALPHA)
            pygame.draw.rect(hover_surf, (255, 255, 255, 40), hover_surf.get_rect(), border_radius=12)
            screen.blit(hover_surf, hover_rect)

        screen.blit(self.image, self.rect)
        font = get_font(font_size)
        text = font.render(self.artist_name, True, "white")
        text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + self.radius + font_size))
        screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        distance = math.hypot(mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        if distance <= self.radius:
            self.selected = not self.selected
            return True
        return False

def get_artist_positions(screen_w, screen_h):
    positions = []
    top_y = int(screen_h * 0.35)
    top_spacing = screen_w // 4
    top_start_x = (screen_w // 2) - top_spacing
    for i in range(3):
        x = top_start_x + i * top_spacing
        positions.append((x, top_y))
    bottom_y = int(screen_h * 0.55)
    bottom_spacing = screen_w // 3
    bottom_start_x = (screen_w // 2) - bottom_spacing // 2
    for i in range(2):
        x = bottom_start_x + i * bottom_spacing
        positions.append((x, bottom_y))
    return positions

def select_artist(screen, player_num, quit_callback):
    """Show artist selection for one player, return chosen artists."""
    screen_w, screen_h = screen.get_size()

    # Dynamic scaling
    base_size = screen_w // 12
    radius = base_size // 2
    font_size = screen_w // 60

    artist_images = load_artist_images(base_size)

    OPTIONS = ARTIST_OPTIONS_A if player_num == 1 else ARTIST_OPTIONS_B
    OPTIONS = [artist.split(" ")[0] for artist in OPTIONS]

    artist_circles = [
        ArtistCircle(pos, artist, radius, artist_images.get(artist))
        for pos, artist in zip(get_artist_positions(screen_w, screen_h), OPTIONS)
    ]

    next_button = Button(
        image=None,
        pos=(screen_w // 2, int(screen_h * 0.8)),
        text_input="NEXT",
        font=get_font(screen_w // 30),
        base_color="White",
        hovering_color="Green"
    )

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        # Scale background
        bg_scaled = pygame.transform.scale(BG, (screen_w, screen_h))
        screen.blit(bg_scaled, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()

        # Title
        title_text = get_font(screen_w // 15).render(f"Player {player_num}", True, "#ffffff")
        title_rect = title_text.get_rect(center=(screen_w // 2, screen_h // 10))
        screen.blit(get_font(screen_w // 15).render(f"Player {player_num}", True, "#000000"), (title_rect.x+2, title_rect.y+2))
        screen.blit(title_text, title_rect)

        # Instructions
        selected_count = sum(1 for c in artist_circles if c.selected)
        instruction_color = "#00ff64" if selected_count == 2 else "#ffffff"
        instruction_text = get_font(screen_w // 30).render(f"Select 2 Artists ({selected_count}/2)", True, instruction_color)
        instruction_rect = instruction_text.get_rect(center=(screen_w // 2, screen_h // 6))
        screen.blit(instruction_text, instruction_rect)

        # Draw circles
        for circle in artist_circles:
            circle.update(MOUSE_POS)
            circle.draw(screen, font_size)

        # Button only visible when ready
        if selected_count == 2:
            next_button.changeColor(MOUSE_POS)
            next_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_callback()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for circle in artist_circles:
                    if circle.handle_click(MOUSE_POS):
                        selected_circles = [c for c in artist_circles if c.selected]
                        if len(selected_circles) > 2:
                            for c in artist_circles:
                                if c.selected and c != circle:
                                    c.selected = False
                                    break
                if selected_count == 2 and next_button.checkForInput(MOUSE_POS):
                    return [circle.artist_name for circle in artist_circles if circle.selected]

        pygame.display.update()
