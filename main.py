import libtcodpy as libtcod
from game import *
import input
import render


def play_game(game):
    while not libtcod.console_is_window_closed():
        render.render_all(game)

        if game.state == 'pathing':
            if game.player.mover.takepath() == 'empty':
                game.state = 'playing'
            game.map_movement = True


        player_action = input.handle_keys(game)

        # If 'tookturn' is added, fov_recompute should be true.

        if player_action == "exit":
            break

dgame = Game()

libtcod.sys_set_fps(30)
libtcod.console_blit(dgame.canvas, 0, 0, CONSOLE_WIDTH, CONSOLE_HEIGHT, 0, 0, 0, 1.0, 1.0)
libtcod.console_flush()
play_game(dgame)