import pygame
import math

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, start_tile, direction, move_key, tiles, kind, size=(100, 100)):
        super().__init__()
        # Load and scale the image to the desired size
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_tile.rect.center)
        self.tile = start_tile
        self.direction = direction
        self.move_key = move_key
        self.tiles = tiles
        self.kind = kind
        self.score = 0

    def update(self, pressed_keys):
        # Rotate constantly
        self.direction = (self.direction + 3) % 360  # 3 degrees per frame
        self.image = pygame.transform.rotate(self.original_image, -self.direction)
        self.rect = self.image.get_rect(center=self.tile.rect.center)

        # Move forward if key pressed
        if pressed_keys[self.move_key]:
            dx = round(math.cos(math.radians(self.direction)))
            dy = round(math.sin(math.radians(self.direction)))
            new_x = self.tile.x + dx
            new_y = self.tile.y + dy
            # Find the tile at new_x, new_y
            for t in self.tiles.inner:
                if t.x == new_x and t.y == new_y:
                    self.tile = t
                    self.rect = self.image.get_rect(center=t.rect.center)
                    if t.kind_of_tile == self.kind:
                        self.score += 1
                    break