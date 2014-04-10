import libtcodpy as libtcod
import actors

# These two objects record input and are checked appropriately.
key = libtcod.Key()
mouse = libtcod.Mouse()


def handle_keys(game):

    libtcod.console_flush()

    event = libtcod.sys_check_for_event(1|4|8|16, key, mouse)
    mousestatus = libtcod.mouse_get_status()

    (a, b) = game.upper_left_of_map()
    (x, y) = (mousestatus.cx + a, mousestatus.cy + b)

    #If the player clicks an acceptable tile, build a path to that location and start pathing toward it.
    if mousestatus.lbutton_pressed and libtcod.map_is_in_fov(game.fov_map, x, y):
        game.state = 'pathing'
        game.player.mover.path = libtcod.path_new_using_map(game.fov_map, 1.41)
        libtcod.path_compute(game.player.mover.path, game.player.x, game.player.y, x, y)

    # Full screen / window switching
    if key.vk == libtcod.KEY_ENTER and (key.lalt | key.ralt): libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # This is a catch-all for situations where one needs to 'back out' of wherever one is.
    # An obvious one is to quit the game.
    if key.vk == libtcod.KEY_ESCAPE:
        return 'exit'

    # Movement keys - used if actually playing.
    if game.state == 'playing':

        dx=dy=0

        key_char = chr(key.c)

        if key_char in ('q','w','e'):
            dy = -1

        if key_char in ('q','a','z'):
            dx = -1

        if key_char in ('z','x','c'):
            dy = 1

        if key_char in ('c','d','e'):
            dx = 1

        if key.vk == libtcod.KEY_UP:
            dy = -1

        elif key.vk == libtcod.KEY_DOWN:
            dy = 1

        elif key.vk == libtcod.KEY_LEFT:
            dx = -1

        elif key.vk == libtcod.KEY_RIGHT:
            dx = 1

        elif key_char in ('1'):
            game.debug_showexplored = not(game.debug_showexplored)

        elif key_char in ('2'):
            game.debug_troubletiles = not(game.debug_troubletiles)

        # Eventually, need keys for working with inventory and items.

        if (dx | dy):
            action = actors.player_move(game, dx, dy)
            if action is not 'blocked':
                game.map_movement = True
                return 'tookturn'

    elif game.state == 'in menu': pass

    else: return 'no action'
