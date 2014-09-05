import libtcodpy as libtcod
import map
import random


class Object:
    # This is a generic object that can be placed or manipulated.
    def __init__(self, x, y, char, name, color, blocks=False, lightsource=None, mover=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks

        self.lightsource = lightsource
        if self.lightsource: # let the lightsource component know who owns it
            self.lightsource.owner = self

        self.mover = mover
        if self.mover: # Let the mover know who owns it
            self.mover.owner = self


class Mover():
    def __init__(self):
        self.path = None

    def move(self, game, dx, dy):
        if not game.is_blocked(self.owner.x+dx, self.owner.y+dy):
            self.owner.x += dx
            self.owner.y += dy
        else:
            return 'blocked'

    def takepath(self):
        #libtcod.path_compute(game.player.path, game.player.destination[0], game.player.destination[1], ...)
        if libtcod.path_is_empty(self.path):
            return 'empty'
        else:
            x,y = libtcod.path_get(self.path, 0)
            self.owner.x, self.owner.y = libtcod.path_walk(self.path,True)
            return 'pathing'

class LightSource():
    def __init__(self, levelmap, style="torch", mobile=False):
        if style == "brazier":
            radius = 20
        else:
            style = "torch"
            radius = 12
        self.style = style
        self.radius = radius
        self.flickerexponent = 0.8
        self.flicker()
        self.mobile = mobile
        self.fov_map = map.new_fov_map(levelmap)

    def flicker(self):
        if self.style == "brazier" or self.style == "torch":
            flicker_variable = random.uniform(-0.1, 0.1)
            if self.flickerexponent + flicker_variable > 0.8:
                self.flickerexponent = 0.8
            elif self.flickerexponent + flicker_variable < 0.5:
                self.flickerexponent = 0.5
            else:
                self.flickerexponent += flicker_variable


def player_move(game, dx, dy):
    target = None

    # Target destination
    x = game.player.x + dx
    y = game.player.y + dy

    # Is there something to attack there?
    for thing in game.objects:
        if thing.x == x and thing.y == y:
            target = thing
            break

    # If so, attack it
    if target is not None:
        return 'attacking'

    # Nothing there, so can we move?
    else:
        moved = game.player.mover.move(game, dx, dy)
        if moved == 'blocked':
            return moved
        else:
            game.fov_recompute = True
            return 'moved'