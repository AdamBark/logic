# This file is part of logic.

# logic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# logic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with logic.  If not, see <http://www.gnu.org/licenses/>.

import os
import pyglet
from pyglet.window import key
from pyglet.gl import *


def load_block_images():
    return {"blank": pyglet.resource.image("blank.png"),
            "and": pyglet.resource.image("and.png"),
            "or": pyglet.resource.image("or.png")}

def get_logic_blocks(images):
    return {key._0: images["blank"], key.NUM_0: images["blank"],
            key._1: images["and"], key.NUM_1: images["and"],
            key._2: images["or"], key.NUM_2: images["or"]}


def fill_block_grid(logic_blocks, start=(0, 112), step=-16):
    block_batch = pyglet.graphics.Batch()
    offset = 0
    sprites = []
    for block in logic_blocks:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        sprites.append(pyglet.sprite.Sprite(block, x=start[0],
                                            y=start[1]+offset,
                                            batch=block_batch))
        offset += step
    return block_batch, sprites


def make_connecting_line(start, finish, colour=(255, 0, 0)):
    offset = 4
    second = (finish[0] - offset, start[1])
    third = (finish[0] - offset, finish[1])
    return pyglet.graphics.vertex_list(6,
                                       ("v2i", (start[0], start[1],
                                                second[0], second[1],
                                                second[0], second[1],
                                                third[0], third[1],
                                                third[0], third[1],
                                                finish[0], finish[1])),
                                       ("c3B", colour*6))


def main():
    BOARD_MIN_X = 16
    BOARD_MAX_X = 112 + BOARD_MIN_X
    BOARD_MIN_Y = 0
    BOARD_MAX_Y = 112 + BOARD_MIN_Y
    BOARD_STEP = 16
    SCALE = 4
    WIN_X = 128 + 16
    WIN_Y = 128
    pyglet.resource.path = ["data"]
    pyglet.resource.reindex()
    window = pyglet.window.Window(WIN_X*SCALE, WIN_Y*SCALE)
    gluOrtho2D(-1.0/SCALE, 1.0/SCALE, -1.0/SCALE, 1.0/SCALE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    selector = pyglet.sprite.Sprite(
        pyglet.resource.image("selector.png"), x=BOARD_MIN_X, y=BOARD_MIN_Y)
    grid = pyglet.resource.image("grid2.png")
    block_grid = pyglet.sprite.Sprite(pyglet.resource.image("block_grid.png"),
                                      x=0, y=0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    block_images = load_block_images()
    logic_blocks = get_logic_blocks(block_images)
    block_batch, block_sprites = fill_block_grid(block_images.values())
    selector.block = pyglet.sprite.Sprite(logic_blocks[key._0])
    num_keys = (key._0, key._1, key._2, key._3, key._4, key._5,
                key._6, key._7, key._8, key._9, key.NUM_0, key.NUM_1,
                key.NUM_2, key.NUM_3, key.NUM_4, key.NUM_5,
                key.NUM_6, key.NUM_7, key.NUM_8, key.NUM_9)
    grid_blocks = [[None]*8 for i in range(8)]

    @window.event
    def on_draw():
        window.clear()
        block_grid.draw()
        block_batch.draw()
        grid.blit(BOARD_MIN_X, BOARD_MIN_Y)
        for row in grid_blocks:
            for block_sprite in row:
                if block_sprite is not None:
                    block_sprite.draw()
        selector.draw()
        selector.block.set_position(selector.x, selector.y)
        selector.block.draw()

    @window.event
    def on_key_press(symbol, modifier):
        if symbol == key.UP:
            selector.y = min(BOARD_MAX_Y, selector.y + BOARD_STEP)
        elif symbol == key.DOWN:
            selector.y = max(BOARD_MIN_Y, selector.y - BOARD_STEP)
        elif symbol == key.LEFT:
            selector.x = max(BOARD_MIN_X, selector.x - BOARD_STEP)
        elif symbol == key.RIGHT:
            selector.x = min(BOARD_MAX_X, selector.x + BOARD_STEP)
        elif symbol in num_keys:
            try:
                selector.block.image = logic_blocks[symbol]
            except KeyError:
                pass
        elif symbol == key.RETURN:
            x = (selector.x - BOARD_MIN_X)//16
            y = (selector.y - BOARD_MIN_Y)//16
            if grid_blocks[x][y]:
                grid_blocks[x][y].image = selector.block.image
            else:
                grid_blocks[x][y] = pyglet.sprite.Sprite(selector.block.image,
                                                         x=selector.x,
                                                         y=selector.y)
    pyglet.app.run()
