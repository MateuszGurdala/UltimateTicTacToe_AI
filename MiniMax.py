from AI import MapMirror
from random import choice


# TODO: fix path bug and alpha-beta pruning

def MiniMax(ai, position, depth, alpha, beta, path, maximizing_player=True):
    """
    position = tuple (game_map, segment_number)
    depth = only odd numbers
    alpha = -inf
    beta = +inf
    """
    game_map = position[0]
    segment_number = position[1]
    current_segment = game_map.segments[segment_number]

    if current_segment.winner:
        if maximizing_player:
            return ai.move_values["won_game"]
        else:
            return ai.move_values["lost_game"]

    if depth == 0 or game_map.winner:
        place_number, place_value = ai.pick_best_move(current_segment, game_map)
        return place_value

    if maximizing_player:
        maximum_evaluation = ai.move_values["lost_game"]

        # Checking possible moves and creating map mirrors after the exact move
        ai.check_possible_moves(current_segment)
        possible_maps = dict()
        for i in ai.possible_moves:
            map_mirror = MapMirror(game_map, segment_number, i, ai.sign)
            possible_maps[i] = map_mirror

        for j in possible_maps:
            evaluation = MiniMax(ai, (possible_maps[j], j), depth - 1, alpha, beta, path, maximizing_player=False)
            path[depth - 1] = (ai.sign, j)

            if evaluation == max(maximum_evaluation, evaluation):
                maximum_evaluation = evaluation

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break

        return maximum_evaluation

    else:
        minimum_evaluation = ai.move_values["won_game"]

        # Checking possible moves and creating map mirrors after the exact move
        ai.check_possible_moves(current_segment)
        possible_maps = dict()
        for i in ai.possible_moves:
            map_mirror = MapMirror(game_map, segment_number, i, ai.enemy_sign)
            possible_maps[i] = map_mirror

        for j in possible_maps:
            evaluation = MiniMax(ai, (possible_maps[j], j), depth - 1, alpha, beta, path, maximizing_player=True)
            path[depth - 1] = (ai.enemy_sign, j)

            if evaluation == min(minimum_evaluation, evaluation):
                minimum_evaluation = evaluation

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return minimum_evaluation


def MiniMax_old(ai, position, depth, path, maximizing_player=True):
    """
    position = tuple (game_map, segment_number)
    depth = only odd numbers
    alpha = -inf
    beta = +inf
    """
    game_map = position[0]
    segment_number = position[1]
    current_segment = game_map.segments[segment_number]

    if current_segment.winner:
        if maximizing_player:
            return ai.move_values["won_game"]
        else:
            return ai.move_values["lost_game"]

    if depth == 0 or game_map.winner:
        place_number, place_value = ai.pick_best_move(current_segment, game_map)
        return place_value

    if maximizing_player:
        maximum_evaluation = ai.move_values["lost_game"]

        # Checking possible moves and creating map mirrors after the exact move
        ai.check_possible_moves(current_segment)
        possible_maps = dict()
        for i in ai.possible_moves:
            map_mirror = MapMirror(game_map, segment_number, i, ai.sign)
            possible_maps[i] = map_mirror

        for j in possible_maps:
            evaluation = MiniMax_old(ai, (possible_maps[j], j), depth - 1, path, maximizing_player=False)

            if evaluation == max(maximum_evaluation, evaluation):
                path[depth - 1] = (ai.sign, j)
                maximum_evaluation = evaluation

        return maximum_evaluation

    else:
        minimum_evaluation = ai.move_values["won_game"]

        # Checking possible moves and creating map mirrors after the exact move
        ai.check_possible_moves(current_segment)
        possible_maps = dict()
        for i in ai.possible_moves:
            map_mirror = MapMirror(game_map, segment_number, i, ai.enemy_sign)
            possible_maps[i] = map_mirror

        for j in possible_maps:
            evaluation = MiniMax_old(ai, (possible_maps[j], j), depth - 1, path, maximizing_player=True)

            if evaluation == min(minimum_evaluation, evaluation):
                path[depth - 1] = (ai.enemy_sign, j)
                minimum_evaluation = evaluation

        return minimum_evaluation
