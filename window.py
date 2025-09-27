"""
Draws a window filled with tiles
"""
import pygame
import constants as con
import os
from generate_grid import *

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
    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        generante_map_file(TILES_HORIZONTAL,TILES_VERTICAL)
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BG_COLOR = con.LIGHTGREY
        self.keep_looping = True
        # ----
        self.tiles = Tiles(self.surface)

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
        self.surface.fill(self.BG_COLOR)
        self.tiles.draw(self.surface)
        pygame.display.update()

    def main(self):
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    mygame = Game()
    mygame.main()