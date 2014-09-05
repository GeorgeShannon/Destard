# Intended for listing what elements are needed for a level.  'levelset' below details the features that are required
# and decided upon.

import random
import roommaking
import actors
import libtcodpy as libtcod


def choose_levelset(level):

    levellist=[]

    if level==1:
        levellist.append("entrance")

    maxtemple = random.randrange(3,5)
    for num in range(0, maxtemple):
        levellist.append("temple")

    #levellist.append("complex")

    return levellist


def select_elements(itemtype):
    # There are several choices here, with different requirements.  The item is chosen from the roommaking set, a
    # chamber is made, and added to the map as well as the room listing.
    if itemtype == "entrance":
        roomselection = random.choice(roommaking.starting.keys())
        layoutselection = roommaking.starting[roomselection]
    else:
        roomselection = random.choice(roommaking.templefurniture.keys())
        layoutselection = roommaking.templefurniture[roomselection]

    return layoutselection


def set_element_values(itemtype, layoutselection, mapwidth, mapheight):
    # Given an item, make some choices about how it's

    # Get the width and heigh
    w, h = roommaking.measurements(layoutselection)

    # Find a spot without going off the edge of the map
    x = random.randrange(0, mapwidth - w - 1)
    y = random.randrange(0, mapheight - h - 1)

    return (x, y, w, h, itemtype)


def dig_room(map, room, layout):
    # go through the tiles in the defined rectangle and construct them according to the layout
    x = room.x1 + 1
    y = room.y1
    for char in layout:
        if char == ".":
            map[x][y].permanent = True
            map[x][y].blocked = False
            map[x][y].block_sight = False
        if char == ",":
            map[x][y].permanent = False
            map[x][y].blocked = False
            map[x][y].block_sight = False
        if char == "X":
            map[x][y].permanent = True
            map[x][y].blocked = True
            map[x][y].block_sight = True
        if char == "x":
            map[x][y].permanent = False
            map[x][y].blocked = True
            map[x][y].block_sight = True
        x += 1
        if char == "\n":
            x = room.x1 + 1
            y += 1

def collect_features(map, room, layout):
    levelobjects = []
    # Go through the layout map, determine proper locations, make the right object for attachment to the level.
    x = room.x1 + 1
    y = room.y1
    for char in layout:
        if char == "b":
            light = actors.LightSource(map, "brazier")
            object = actors.Object(x, y, 'x', 'brazier', libtcod.black, blocks=True, lightsource=light)
            levelobjects.append(object)
        x += 1
        if char == "\n":
            x = room.x1 + 1
            y += 1
    return levelobjects
