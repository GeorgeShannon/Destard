import libtcodpy as libtcod
import math
import menu
import random

FOV_LIGHT_WALLS = True
FOV_ALGORITHM = 0

color_dark_wall = libtcod.Color(40, 40, 40)
color_light_wall = libtcod.Color(100, 100, 100)
color_dark_ground = libtcod.Color(20, 20, 20)
color_light_ground = libtcod.Color(200, 180, 50)
color_unexplored = libtcod.Color(10, 10, 20)

def render_all(game):

    # Get the location for the upper left corner of the screen
    [a,b] = game.upper_left_of_map()

    # Build map for viewing
    render_view(game,a,b)

    # Build object identifiers
    render_objects(game)

    libtcod.console_blit(game.canvas, a, b, game.canvas_width, game.canvas_height, 0, 0, 0)

    libtcod.console_flush()

    # Erase all objects at their old locations, before they move
    for thing in game.objects:
        libtcod.console_put_char(game.canvas, thing.x, thing.y, ' ', libtcod.BKGND_NONE)

    # This displays interface elements
    #game.interface.blit_panels(game)

def render_view(game,a,b):
    # A shortcut since player location is used quite a bit.
    px = game.player.x
    py = game.player.y

    # In cases where things have moved or the map has changed, recompute the FOV.  Otherwise we just need to re-render for lighting effects.
    if game.map_change:
        for object in game.objects:
            if object.lightsource:
                libtcod.map_compute_fov(object.lightsource.fov_map, object.x, object.y, object.lightsource.radius, FOV_LIGHT_WALLS, FOV_ALGORITHM)
                libtcod.map_compute_fov(game.fov_map, px, py, 30, FOV_LIGHT_WALLS, FOV_ALGORITHM)
    elif game.map_movement:
        for object in game.objects:
            if object.lightsource and object.lightsource.mobile:
                libtcod.map_compute_fov(object.lightsource.fov_map, object.x, object.y, object.lightsource.radius, FOV_LIGHT_WALLS, FOV_ALGORITHM)
                libtcod.map_compute_fov(game.fov_map, px, py, 40, FOV_LIGHT_WALLS, FOV_ALGORITHM)

    game.map_movement = False
    game.map_change = False

    for c in range(game.width - menu.reserved_width()):
        for d in range(game.height - menu.reserved_height()):
            x = a + c
            y = b + d

            #We need to check these map locations to see if they are visible to the player, first of all, and if they
            #  are, include effects from all light sources.
            visible = libtcod.map_is_in_fov(game.fov_map, x, y)
            wall = game.map[x][y].block_sight

            if not visible: # If it's not visible, we don't care how well it's lit, just whether it's explored.
                if game.map[x][y].explored or game.debug_showexplored: # Is it something worth showing?
                    if wall:
                        libtcod.console_set_char_background(game.canvas, x, y, color_dark_wall, libtcod.BKGND_SET)
                        libtcod.console_set_default_foreground(game.canvas, color_dark_ground)
                        libtcod.console_put_char(game.canvas, x, y, libtcod.CHAR_BLOCK2, libtcod.BKGND_NONE)
                    else: libtcod.console_set_char_background(game.canvas, x, y, color_dark_ground, libtcod.BKGND_SET)
                else: # Otherwise just make that tile the unexplored color.
                    libtcod.console_set_char_background(game.canvas, x, y, color_unexplored, libtcod.BKGND_SET)
            else: # must be visible, let's check on light sources
                lerpfactor = 0
                for object in game.objects:
                     # This checks whether the object is a lightsource and can 'see' the tile in question.
                    if object.lightsource and libtcod.map_is_in_fov(object.lightsource.fov_map, x, y):
                        distance=math.sqrt((x - object.x)**2 + (y - object.y)**2)
                        if distance <= object.lightsource.radius:
                            lerpfactor += 1-( distance / object.lightsource.radius ) ** object.lightsource.flickerexponent
                game.map[x][y].explored = True
                if lerpfactor>1: lerpfactor=1
                if wall:
                    libtcod.console_set_char_background(game.canvas, x, y, libtcod.color_lerp(color_light_wall, color_dark_wall, 1-lerpfactor), libtcod.BKGND_SET)
                    libtcod.console_set_default_foreground(game.canvas, color_dark_ground)
                    libtcod.console_put_char(game.canvas, x, y, libtcod.CHAR_BLOCK2, libtcod.BKGND_NONE)
                else: libtcod.console_set_char_background(game.canvas, x, y, libtcod.color_lerp(color_light_ground, color_dark_ground, 1-lerpfactor), libtcod.BKGND_SET)





                #fromplayerdist = ( math.sqrt( (x - px)**2 + (y - py)**2 ) / game.torch_radius ) ** game.torch_flicker_exponent
                #game.map[x][y].explored = True
                #if wall: libtcod.console_set_char_background(game.canvas, x, y, libtcod.color_lerp(color_light_wall, color_dark_wall, fromplayerdist), libtcod.BKGND_SET)
                #else: libtcod.console_set_char_background(game.canvas, x, y, libtcod.color_lerp(color_light_ground, color_dark_ground, fromplayerdist), libtcod.BKGND_SET)

    # Draws out tiles that have been flagged as troublesome, for whatever reason (such as carving permanent tiles)
    if game.debug_troubletiles:
        for c in range(game.width - menu.reserved_width()):
            for d in range(game.height - menu.reserved_height()):
                x = a + c
                y = b + d
                if game.map[x][y].debug:
                    libtcod.console_set_char_background(game.canvas, x, y, libtcod.dark_purple, libtcod.BKGND_SET)
        #libtcod.console_print(game.canvas, 0,0, "This is a test string")

    # Also need to update the light source change
    #game.torch_flicker_exponent = game.torch_flicker_exponent + random.uniform(-0.1, 0.1)
    #if game.torch_flicker_exponent < 0.5: game.torch_flicker_exponent=0.5
    #if game.torch_flicker_exponent > 1: game.torch_flicker_exponent=1
    for object in game.objects:
            if object.lightsource:
                object.lightsource.flicker()


def render_objects(game):
    # Draw non-player things before player
    for thing in game.objects:
        if thing != game.player:
            draw(game.canvas, game.player.lightsource.fov_map, thing)
    draw(game.canvas, game.player.lightsource.fov_map, game.player)


def draw(console, fov_map, thing):
    # Only draw when in FOV
    if libtcod.map_is_in_fov(fov_map, thing.x, thing.y):
        libtcod.console_set_default_foreground(console, thing.color)
        libtcod.console_put_char(console, thing.x, thing.y, thing.char, libtcod.BKGND_NONE)