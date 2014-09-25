import libtcodpy as libtcod
from mapmaking import *
import actors

# Map size.
MAP_WIDTH = 100
MAP_HEIGHT = 80


def new_level(levelnum):
    level = FullMap(MAP_WIDTH, MAP_HEIGHT, levelnum, 0.42)
    return level

def get_map_from_level(game):
    map = game.level.finalize_map()
    game.map_width = MAP_WIDTH
    game.map_height = MAP_HEIGHT
    return map

def get_objects_from_level(game):
    objects = game.level.finalize_obects()
    return objects
   
#def get_rooms(factory):
 #   rooms = factory.get_rooms()
  #  return rooms
   
# Place the player in one of the rooms generated by the cave factory.
def initial_place_player(game):
    while True:
        rooms = game.level.get_rooms()
        numrooms = len(rooms)-1
        game.level.check_open()
        room = rooms[libtcod.random_get_int(0, 0, numrooms)]
    
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        if not game.map[x][y].blocked:
            game.player.x = x
            game.player.y = y
            break


# An FOV map built using a provided map.
def new_fov_map(map):
    width = MAP_WIDTH
    height = MAP_HEIGHT
    fov_map = libtcod.map_new(width, height)
    for y in range(height):
        for x in range(width):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
    return fov_map


# This is for pathing - the path should depend on whether the area is explored or not.
def new_fov_pathing_map(map):
    width = MAP_WIDTH
    height = MAP_HEIGHT
    fov_pathing_map = libtcod.map_new(width, height)
    for y in range(height):
        for x in range(width):
            libtcod.map_set_properties(fov_pathing_map, x, y, not map[x][y].block_sight, (not map[x][y].blocked and map[x][y].explored))
    return fov_pathing_map


# An internal check for whether a map tile is blocked (by a wall)
def is_blocked(map, x, y):
    # first test the map tile
    if map[x][y].blocked:
        return True
    return False