import pygame, sys
import os
import math
from assets.menu.button import Button
from backend import ARTIST_OPTIONS_A, ARTIST_OPTIONS_B

pygame.init()

# Get the current directory where the script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Artist Selection")

# Use os.path.join for file paths
BG = pygame.image.load(os.path.join(CURRENT_DIR, "assets", "menu", "Background.png"))

def get_font(size):
    return pygame.font.Font(os.path.join(CURRENT_DIR, "assets", "menu", "font.ttf"), size)

def load_artist_images():
    """Preload all artist images with optimization"""
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
            # Load and immediately convert to display format for better performance
            original = pygame.image.load(path).convert_alpha()
            # Pre-scale to the size we'll use (140x140)
            scaled = pygame.transform.scale(original, (140, 140))
            images[artist] = scaled
        except pygame.error:
            print(f"Failed to load image for {artist}")
            # Create fallback surface
            surface = pygame.Surface((140, 140), pygame.SRCALPHA)
            pygame.draw.circle(surface, (100, 100, 100), (70, 70), 65)
            pygame.draw.circle(surface, (150, 150, 150), (70, 70), 65, 3)
            images[artist] = surface
    return images

# Load images once at startup
ARTIST_IMAGES = load_artist_images()

class ArtistCircle:
    def __init__(self, pos, artist_name):
        self.pos = pos
        self.artist_name = artist_name
        self.radius = 70
        self.selected = False
        self.hover = False
        self.pulse_offset = 0
        
        # Use preloaded image
        if artist_name in ARTIST_IMAGES:
            self.image = ARTIST_IMAGES[artist_name]
        else:
            # Fallback for missing artists
            self.image = pygame.Surface((140, 140), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, 140, 140))
            pygame.draw.rect(self.image, (150, 150, 150), (0, 0, 140, 140), 3)
        
        self.rect = self.image.get_rect(center=pos)

    # Remove the circular image creation method completely

    def update(self, mouse_pos):
        """Update hover state and animations"""
        distance = math.sqrt((mouse_pos[0] - self.pos[0])**2 + (mouse_pos[1] - self.pos[1])**2)
        self.hover = distance <= self.radius
        
        # Update pulse animation for selected items
        if self.selected:
            self.pulse_offset = (self.pulse_offset + 0.15) % (2 * math.pi)

    def draw(self, screen):
        # Draw selection border FIRST (under the image)
        if self.selected:
            # Pulsing glow effect
            pulse_intensity = 0.7 + 0.3 * math.sin(self.pulse_offset)
            border_color = (int(0 * pulse_intensity), int(255 * pulse_intensity), int(100 * pulse_intensity))
            
            # Draw selection square with rounded corners
            border_size = 150  # Slightly larger than the image (140x140)
            border_rect = pygame.Rect(0, 0, border_size, border_size)
            border_rect.center = self.pos
            
            # Draw multiple layers for glow effect
            for i in range(3):
                alpha = int(120 * pulse_intensity * (3-i) / 3)
                glow_size = border_size + i * 6
                glow_rect = pygame.Rect(0, 0, glow_size, glow_size)
                glow_rect.center = self.pos
                
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*border_color, alpha), glow_surf.get_rect(), border_radius=15)
                screen.blit(glow_surf, glow_rect)
            
            # Draw main border
            pygame.draw.rect(screen, border_color, border_rect, width=4, border_radius=12)
            
            # Inner highlight
            inner_rect = border_rect.inflate(-6, -6)
            pygame.draw.rect(screen, (255, 255, 255, 80), inner_rect, width=2, border_radius=10)
        
        elif self.hover:
            # Subtle hover effect with square
            hover_size = 145
            hover_rect = pygame.Rect(0, 0, hover_size, hover_size)
            hover_rect.center = self.pos
            
            hover_surf = pygame.Surface((hover_size, hover_size), pygame.SRCALPHA)
            pygame.draw.rect(hover_surf, (255, 255, 255, 40), hover_surf.get_rect(), border_radius=12)
            screen.blit(hover_surf, hover_rect)
        
        # Draw artist image (square) - NOW ON TOP
        screen.blit(self.image, self.rect)
        
        # Draw artist name below WITHOUT background
        font = get_font(18)
        text = font.render(self.artist_name, True, "white")
        text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + self.radius + 40))
        
        # Draw text directly without background
        screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        distance = math.sqrt((mouse_pos[0] - self.pos[0])**2 + (mouse_pos[1] - self.pos[1])**2)
        if distance <= self.radius:
            self.selected = not self.selected
            return True
        return False

def get_artist_positions():
    """Calculate positions for 3 artists on top, 2 on bottom layout with more spacing"""
    positions = []
    
    # Top row (3 artists) - increased spacing
    top_y = 280
    top_spacing = 250  # Increased from 200 to 250
    top_start_x = 640 - top_spacing  # Center the 3 artists
    
    for i in range(3):
        x = top_start_x + i * top_spacing
        positions.append((x, top_y))
    
    # Bottom row (2 artists) - increased spacing
    bottom_y = 480  # Moved down from 450 to 480
    bottom_spacing = 250  # Increased from 200 to 250
    bottom_start_x = 640 - bottom_spacing // 2  # Center the 2 artists
    
    for i in range(2):
        x = bottom_start_x + i * bottom_spacing
        positions.append((x, bottom_y))
    
    return positions

def select_artists(player_num, artist_list):
    selected_artists = []
    
    # Create artist circles with better positioning
    artist_circles = []
    positions = get_artist_positions()
    
    for i, artist in enumerate(artist_list):
        artist_circles.append(ArtistCircle(positions[i], artist))

    next_button = Button(image=None, pos=(640, 650),
                        text_input="NEXT", font=get_font(40),
                        base_color="White", hovering_color="Green")
    
    clock = pygame.time.Clock()

    while True:
        # Cap FPS for smoother performance
        clock.tick(60)
        
        SCREEN.blit(BG, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()

        # Draw title with better styling
        title_text = get_font(80).render(f"Player {player_num}", True, "#ffffff")
        title_rect = title_text.get_rect(center=(640, 80))
        
        # Add title shadow
        shadow_text = get_font(80).render(f"Player {player_num}", True, "#000000")
        shadow_rect = shadow_text.get_rect(center=(642, 82))
        SCREEN.blit(shadow_text, shadow_rect)
        SCREEN.blit(title_text, title_rect)

        # Draw instruction with styling
        selected_count = sum(1 for circle in artist_circles if circle.selected)
        instruction_color = "#00ff64" if selected_count == 2 else "#ffffff"
        instruction_text = get_font(35).render(f"Select 2 Artists ({selected_count}/2)", True, instruction_color)
        instruction_rect = instruction_text.get_rect(center=(640, 150))
        SCREEN.blit(instruction_text, instruction_rect)

        # Update and draw all artist circles
        for circle in artist_circles:
            circle.update(MOUSE_POS)
            circle.draw(SCREEN)

        # Update next button (only show when 2 artists selected)
        if selected_count == 2:
            next_button.changeColor(MOUSE_POS)
            next_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle artist selection
                for circle in artist_circles:
                    if circle.handle_click(MOUSE_POS):
                        # If selecting a new artist and already have 2, deselect oldest
                        selected_circles = [c for c in artist_circles if c.selected]
                        if len(selected_circles) > 2:
                            # Find the one we just clicked and keep it selected
                            # Deselect the first one that isn't the one we just clicked
                            for c in artist_circles:
                                if c.selected and c != circle:
                                    c.selected = False
                                    break
                
                # Handle next button
                if selected_count == 2 and next_button.checkForInput(MOUSE_POS):
                    return [circle.artist_name for circle in artist_circles if circle.selected]

        pygame.display.update()

def show_loading_screen():
    """Show a loading screen while initializing"""
    SCREEN.blit(BG, (0, 0))
    
    loading_text = get_font(60).render("Loading Artists...", True, "#ffffff")
    loading_rect = loading_text.get_rect(center=(640, 360))
    SCREEN.blit(loading_text, loading_rect)
    
    pygame.display.update()

def main_menu():
    # Show loading screen
    show_loading_screen()
    
    # First select artists for Player 1
    OPTIONS_A = [artist.split(" ")[0] for artist in ARTIST_OPTIONS_A]
    OPTIONS_B = [artist.split(" ")[0] for artist in ARTIST_OPTIONS_B]
    player1_artists = select_artists(1, OPTIONS_A)
    print("Player 1 selected:", player1_artists)
    
    # Then select artists for Player 2
    player2_artists = select_artists(2, OPTIONS_B)
    print("Player 2 selected:", player2_artists)
    
    # Here you can proceed to the next game state with the selected artists
    return player1_artists, player2_artists

if __name__ == "__main__":
    main_menu()