"""
Draws a window filled with tiles
"""
import pygame
import sys
import constants as con
from generate_grid import generante_map_file
from menu_page import main_menu
from select_artist import select_artist
import os
from backend import *
import time
from sprite import *


#helpers
def play_preview(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play() 


def download_music():
    pass

TITLE = "Mashup Mania"
TILES_HORIZONTAL = 8
TILES_VERTICAL = 5
TILESIZE = 180
WINDOW_WIDTH = TILESIZE * TILES_HORIZONTAL
WINDOW_HEIGHT = TILESIZE * TILES_VERTICAL

# --------------------------------------------------------
#                   class Tile
# --------------------------------------------------------

class Tile:
    def __init__(self, id, x, y, kind_of_tile):
        filename = ""
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.kind_of_tile = kind_of_tile
        # ----
        if kind_of_tile == "a": filename = con.ALBUM_A
        elif kind_of_tile == "b" : filename = con.ALBUM_B
        elif kind_of_tile == "n" : filename = con.NEUTRAL
        else: raise ValueError("Error! kind of tile: ", kind_of_tile)
        # ---------------------
        self.rect = pygame.Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = "assets/images"
        self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        s = "id: {}, x: {}, y: {}, kind: {}"
        s = s.format(self.id, self.x, self.y, self.kind_of_tile)
        print(s)

# --------------------------------------------------------
#                   class Tiles
# --------------------------------------------------------

class Tiles:
    def __init__(self, screen):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self._load_data()

    def _load_data(self):
        self.inner = []
        filepath = "assets/map.txt"
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        id = 0
        for count_i, myline in enumerate(mylines):
            temp_list = myline.split(";")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
            for count_j, elem in enumerate(temp_list):
                new_tile = Tile(id, count_j, count_i, elem)
                self.inner.append(new_tile)
                id += 1

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Doh! There are no tiles to display. 😕")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

# --------------------------------------------------------
#                   class Game
# --------------------------------------------------------

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.keep_looping = True
        # ----
        self.tiles = Tiles(self.screen)

        #music assets
        self.current_music_state = "game"  # initial state
        self.last_music_state = None
        # preloaded file paths for demo
        self.file_game = "assets/music/game_score.mp3"
        self.file_a = "assets/music/player_a.mp3"
        self.file_b = "assets/music/player_b.mp3"


        #sprites
        start_tile_a = self.tiles.inner[0]
        start_tile_b = self.tiles.inner[-1]
        self.player_a = PlayerSprite("assets/character_sprites/archer.png", start_tile_a, 0, pygame.K_a, self.tiles, "a", size=(120, 120))
        self.player_b = PlayerSprite("assets/character_sprites/Hurt.png", start_tile_b, 180, pygame.K_l, self.tiles, "b", size=(120, 120))
        self.all_sprites = pygame.sprite.Group(self.player_a, self.player_b)
        self.timer_start = time.time()
        self.timer_duration = 30  # seconds

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(con.LIGHTGREY)
        self.tiles.draw(self.screen)
        self.all_sprites.draw(self.screen)  # <-- Draw sprites here!
        # Draw timer
        elapsed = int(time.time() - self.timer_start)
        remaining = max(0, self.timer_duration - elapsed)
        font = pygame.font.SysFont(None, 60)
        timer_surf = font.render(f"Time: {remaining}", True, (0,0,0))
        self.screen.blit(timer_surf, (20, 20))
        pygame.display.update()

    def update_music(self):
        if self.current_music_state != self.last_music_state:
            pygame.mixer.music.stop()
            if self.current_music_state == "game":
                play_preview(self.file_game)
            elif self.current_music_state == "player_a":
                play_preview(self.file_a)
            else:
                play_preview(self.file_b)
            self.last_music_state = self.current_music_state

    # def show_results(self):
    #     # Show winner or tie
    #     font = pygame.font.SysFont(None, 100)
    #     if self.player_a.score > self.player_b.score:
    #         text = "Player A Wins!"
    #     elif self.player_b.score > self.player_a.score:
    #         text = "Player B Wins!"
    #     else:
    #         text = "It's a Tie!"
    #     surf = font.render(text, True, (0,0,0))
    #     rect = surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    #     self.screen.blit(surf, rect)
    #     pygame.display.update()
    #     pygame.time.wait(4000)

    def show_results(self):
        # Semi-transparent pop-up rectangle
        popup_width, popup_height = 800, 400
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Create a surface for the popup
        popup_surf = pygame.Surface((popup_width, popup_height))
        popup_surf.set_alpha(230)  # semi-transparent
        popup_surf.fill((0, 0, 0))  # dark grey background

        # Draw border (pixelated / "gamey")
        border_color = (255, 255, 255)  # yellow border
        border_thickness = 6
        pygame.draw.rect(popup_surf, border_color, popup_surf.get_rect(), border_thickness)

        # Decide winner text
        if self.player_a.score > self.player_b.score:
            text = "Player A Wins!"
        elif self.player_b.score > self.player_a.score:
            text = "Player B Wins!"
        else:
            text = "It's a Tie!"

        # Render the text (big pixel font optional)
        font = pygame.font.Font("assets/menu/font.ttf")
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(popup_width//2, popup_height//2))

        # Blit text onto popup
        popup_surf.blit(text_surf, text_rect)

        # Blit popup onto main screen
        self.screen.blit(popup_surf, (popup_x, popup_y))
        pygame.display.update()

        # Pause to let player read
        pygame.time.wait(4000)


    def main(self):
        clock = pygame.time.Clock()
        while self.keep_looping:
            self.events()
            pressed = pygame.key.get_pressed()
            self.all_sprites.update(pressed)

            for player in [self.player_a, self.player_b]:
                if getattr(player, "music_request", None):
                    self.current_music_state = player.music_request
                    player.music_request = None  # Reset after handling
            self.update_music()
            self.draw()
            # Timer
            elapsed = time.time() - self.timer_start
            if elapsed >= self.timer_duration:
                self.show_results()
                break
            clock.tick(60)

def quit_game():
    pygame.quit()
    sys.exit()

def start_game_flow(screen):
    # Player A selection
    player_a = select_artist(screen, player_num=1, quit_callback=quit_game)
    player_b = select_artist(screen, player_num=2, quit_callback=quit_game)
    download_preview(player_a, 'assets/music/player_a.mp3')
    download_preview(player_b, 'assets/music/player_b.mp3')
    game = Game(screen)
    game.main()

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    generante_map_file(TILES_HORIZONTAL, TILES_VERTICAL)

    file_game = "assets/music/game_score.mp3"
    pygame.mixer.music.load(file_game)
    pygame.mixer.music.play(-1)

    
    main_menu(screen, start_game_flow, quit_game)

if __name__ == "__main__":
    main()