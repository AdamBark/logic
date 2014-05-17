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


def get_logic_blocks():
    blank = pyglet.resource.image("blank.png")
    and_img = pyglet.resource.image("and.png")
    or_img = pyglet.resource.image("or.png")
    return {key._0: blank, key.NUM_0: blank,
            key._1: and_img, key.NUM_1: and_img,
            key._2: or_img, key.NUM_2: or_img}

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
    gluOrtho2D(-1/SCALE, 1/SCALE, -1/SCALE, 1/SCALE)
    block = pyglet.resource.image("logic_block.png")
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    sprite = pyglet.sprite.Sprite(block, x=0, y=0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    selector = pyglet.sprite.Sprite(
        pyglet.resource.image("selector.png"), x=BOARD_MIN_X, y=BOARD_MIN_Y)
    grid = pyglet.resource.image("grid2.png")
    block_grid = pyglet.sprite.Sprite(pyglet.resource.image("block_grid.png"),
                                      x=0, y=0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    logic_blocks = get_logic_blocks()
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
        grid.blit(BOARD_MIN_X, BOARD_MIN_Y)
        sprite.draw()
        selector.draw()
        selector.block.set_position(selector.x, selector.y)
        selector.block.draw()
        for row in grid_blocks:
            for block_sprite in row:
                if block_sprite is not None:
                    block_sprite.draw()

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
