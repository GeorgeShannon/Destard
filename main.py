#import libtcodpy as libtcod
from game import *
import input
import render


def play_game(game):
    while not libtcod.console_is_window_closed():
        render.render_all(game)

        #In the case of pathing, follow the path or switch back to normal playing when done.
        if game.state == 'pathing':
            if game.player.mover.takepath(game) == 'empty':
                game.state = 'playing'
            game.map_movement = True

        if game.map_movement:
            pass # Here we can check to see if player movement has occurred and see if an event should come up.

        player_action = input.handle_keys(game)

        # If 'tookturn' is added, fov_recompute should be true.

        if player_action == "exit":
            break

dgame = Game()

libtcod.sys_set_fps(30)
libtcod.console_blit(dgame.canvas, 0, 0, CONSOLE_WIDTH, CONSOLE_HEIGHT, 0, 0, 0, 1.0, 1.0)
libtcod.console_flush()
play_game(dgame)