"""
Draws a window filled with tiles
"""
import pygame
import sys
import constants as con
from generate_grid import generante_map_file
from menu_page import main_menu
from player_a_selector import player_a_selector
from player_b_selector import player_b_selector
import os
from backend import *


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

    def main(self):
        while self.keep_looping:
            self.events()
            self.update()
            self.update_music()
            self.draw()

def quit_game():
    pygame.quit()
    sys.exit()

def start_game_flow(screen):
    # Player A selection
    player_a = player_a_selector(screen, quit_game)
    if player_a is None:
        player_b = player_b_selector(screen, quit_game)
        if player_b is None:    
            download_music()
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
