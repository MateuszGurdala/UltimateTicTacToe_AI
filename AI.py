from random import choice
import copy
from map_template import *


class AI:
    def __init__(self):
        self.sign = None
        self.enemy_sign = None
        self.possible_moves = dict()  # list of possible moves
        self.next_segment_values = {str(i): 0 for i in range(1, 10)}

        # Point values related to specific situations
        self.move_values = {
            # Ai turn
            "win_segment": 5,
            "block_segment": 4,
            "adjacent": 1,
            "opposite": 1,
            "corner": 0,

            # Enemy turn
            "enemy_win_segment": -5,
            "enemy_block": -4,

            # Following segment
            "finished": -50,
            "ai_place": 1,
            "enemy_place": -1,

            # Whole game map
            "won_game": pow(10, 10),
            "lost_game": -pow(10, 10),
            "won_segment": 5,
            "lost_segment": -5,
            "possible_win": 10,
            "possible_defeat": -10
        }

    def set_sign(self, sign):
        """
        sign = ai's sign
        Automatically sets the enemy sign based on the ai sign
        """
        self.sign = sign
        if self.sign == "X":
            self.enemy_sign = "O"
        else:
            self.enemy_sign = "X"

    def update_move_points(self, place_number, key="", val=0):
        if key:
            self.possible_moves[place_number] = self.possible_moves[place_number] + self.move_values[key]
        elif val:
            self.possible_moves[place_number] = self.possible_moves[place_number] + val

    def update_segment_value(self, segment, key="", val=0):
        if key:
            self.next_segment_values[segment.number] = self.next_segment_values[segment.number] + self.move_values[key]
        elif val:
            self.next_segment_values[segment.number] = self.next_segment_values[segment.number] + val

    @staticmethod
    def return_max(vals_dict):
        """
        returns tuple (number, value)
        """
        ans = []  # Array of highest value numbers
        vals = []  # Array of all values

        for i in vals_dict:
            vals.append(vals_dict[i])
        max_val = max(vals)

        for j in vals_dict:
            if vals_dict[j] == max_val:
                ans.append(j)

        return choice(ans), max_val

    @staticmethod
    def clear_dict(dictionary):
        key = 1
        while key <= 9:
            if str(key) in dictionary and dictionary[str(key)] == "del":
                del dictionary[str(key)]
            key += 1

        return dictionary

    """
    Checking for AI's possible moves and their point values
    Method names represent what they focus on
    """

    def check_possible_moves(self, segment):
        """
        Clears self.possible_moves
        Checks every "free" place in a segment
        """
        self.possible_moves.clear()
        for i in segment.places:
            if not segment.places[i]:  # Checking if place is free
                self.possible_moves[i] = 0

    def adjacent_places(self, segment):
        """
        adjacent -> they are part of a winning combination
        """
        adjacent = {
            "1": list(str(234579)),
            "2": list(str(1358)),
            "3": list(str(125679)),
            "4": list(str(1567)),
            "5": list(str(12346789)),
            "6": list(str(3459)),
            "7": list(str(134589)),
            "8": list(str(2579)),
            "9": list(str(135678))
        }
        for i in segment.places:
            if segment.places[i] == self.sign:  # Check every place with the ai sign
                for j in adjacent[i]:
                    if j in self.possible_moves:  # Update place value if it is adjacent and free
                        self.update_move_points(j, key="adjacent")

    def wins_blocks(self, segment, enemy=False):
        """
        checks every possible win/block combination
        enemy = True when method is used to evaluate the next segment
        """
        if self.check_segment(segment, self.sign):
            wins = self.check_segment(segment, self.sign)
            for i in wins:  # Wins for ai are blocks for the enemy
                if not enemy:
                    self.update_move_points(i, key="win_segment")
                else:
                    self.update_segment_value(segment, key="enemy_block")

        if self.check_segment(segment, self.enemy_sign):
            blocks = self.check_segment(segment, self.enemy_sign)
            for i in blocks:
                if not enemy:
                    self.update_move_points(i, key="block_segment")
                else:
                    self.update_segment_value(segment, key="enemy_win_segment")

    def opposite_places(self, segment):
        """
        opposite -> same place as if segment was rotated 180 degrees
        """
        for i in segment.places:
            if segment.places[i] == self.sign and str(10 - int(i)) in self.possible_moves:
                self.update_move_points(str(10 - int(i)), key="opposite")

    def corners(self):
        for i in list(str(1379)):
            if i in self.possible_moves:
                self.update_move_points(i, key="corner")

    """
    Universal methods
    """

    @staticmethod
    def check_line_of_places(places, sign):
        """
        Checks if two places have the given sign value and the third one is free
        If positive: returns number of the free place, starting from one
        If negative: returns False
        """
        if [places[0], places[1]] == [sign, sign] and not places[2]:
            return 3
        elif [places[0], places[2]] == [sign, sign] and not places[1]:
            return 2
        elif [places[1], places[2]] == [sign, sign] and not places[0]:
            return 1
        return False

    def check_rows(self, segment, sign):
        ans = []
        sp = segment.places
        for i in range(3):
            row = [sp[str(1 + 3 * i)], sp[str(2 + 3 * i)], sp[str(3 + 3 * i)]]  # Going over every row
            if self.check_line_of_places(row, sign):
                ans.append(str(self.check_line_of_places(row, sign) + 3 * i))

        if ans:
            return ans
        return False

    def check_columns(self, segment, sign):
        ans = []
        sp = segment.places
        for i in range(3):
            row = [sp[str(1 + i)], sp[str(4 + i)], sp[str(7 + i)]]  # Going over every column
            place_value = {
                1: list(str(123)),
                2: list(str(456)),  # Place number based on current iteration number and returned place number
                3: list(str(789)),
            }
            if self.check_line_of_places(row, sign):
                ans.append(place_value[self.check_line_of_places(row, sign)][i])

        if ans:
            return ans
        return False

    def check_diagonals(self, segment, sign):
        ans = []
        sp = segment.places
        for i in range(2):
            row = [sp[str(1 + 6 * i)], sp[str(5)], sp[str(9 - 6 * i)]]
            place_value = {
                1: str(1 + 6 * i),
                2: str(5),
                3: str(9 - 6 * i)
            }
            if self.check_line_of_places(row, sign):
                ans.append(place_value[self.check_line_of_places(row, sign)])

        if ans:
            return ans
        return False

    def check_segment(self, segment, sign):
        """
        Checking for possible win/block situations (both segment/map)
        Returns all place numbers as a list (places can repeat)
        If there are none returns False value
        All sub-methods work alike, but in specific situations
        """
        ans = []
        if self.check_rows(segment, sign):
            ans += self.check_rows(segment, sign)
        if self.check_columns(segment, sign):
            ans += self.check_columns(segment, sign)
        if self.check_diagonals(segment, sign):
            ans += self.check_diagonals(segment, sign)

        if ans:
            return ans
        return False

    @staticmethod
    def places(segment, sign):
        """
        Returns number of places with the specific sign
        If there are none returns False
        """
        ans = []
        for i in segment.places:
            if segment.places[i] == sign:
                ans.append(i)

        if ans:
            return ans
        return False

    """
    Checking the next segment
    """

    def places_value(self, segment, enemy=False):
        """
        Updates segment values based on number of ai's/enemy's places
        """
        sign = -1
        if enemy:  # Inverting the value sign for the enemy evaluation
            sign = 1
        if self.places(segment, self.sign):  # Ai places
            ai = self.places(segment, self.sign)
            self.update_segment_value(segment, val=self.move_values["ai_place"] * len(ai) * sign)
        if self.places(segment, self.enemy_sign):  # Enemy places
            enemy = self.places(segment, self.enemy_sign)
            self.update_segment_value(segment, val=self.move_values["enemy_place"] * len(enemy) * sign)

    """
    Checking the whole game map for specific situations
    """

    def possible_win(self, game_map, enemy=False):
        # Checking if segment is in a winnable combination
        if self.check_segment(game_map, sign=self.enemy_sign if enemy else self.sign):
            winning_segments = self.check_segment(game_map, sign=self.enemy_sign if enemy else self.sign)
        else:
            return False

        # Checking if the segment itself is winnable
        for i in winning_segments:
            segment = game_map.segments[i]
            if self.check_segment(segment, sign=self.enemy_sign if enemy else self.sign):
                pass
            else:
                winning_segments.remove(i)

        if winning_segments:
            return winning_segments
        return False

    @staticmethod
    def segment_count(game_map, sign):
        """
        Returns count of segments that are won by the sign
        """
        ans = []
        for i in game_map.places:
            if game_map.places[i] == sign:
                ans.append(i)

        if ans:
            return len(ans)
        return False

    """
    Final evaluation methods
    """

    def evaluate_all_moves(self, segment):
        """
        Evaluates all possible move values based on:
        Possible win/block situations
        Is adjacent to the other one
        Is opposite to the other one
        Is in the corner of the segment
        """
        self.check_possible_moves(segment)
        self.wins_blocks(segment)
        self.adjacent_places(segment)
        self.opposite_places(segment)
        self.corners()

        return self.possible_moves

    def evaluate_next_segment(self, segment, game_map):
        """
        Evaluating the segment that enemy will be moved to
        Value depends on: if finished/ possible win/block situations, ai and enemy place count
        Returns tuple (segment number, segment value)
        """
        num = segment.number
        self.next_segment_values = {str(i): 0 for i in range(1, 10)}
        possible_enemy_win = self.possible_win(game_map, enemy=True)
        if segment.winner:
            # If enemy is one place away from winning the game then letting him choose the segment is certain loss
            if possible_enemy_win:
                self.update_segment_value(segment, key="lost_game")
            else:
                self.update_segment_value(segment, key="finished")
        else:
            # Checking if winning this segment by enemy means losing the game
            if possible_enemy_win and self.check_segment(segment, self.enemy_sign):
                self.update_segment_value(segment, key="lost_game")
            else:
                self.wins_blocks(segment, enemy=True)
                self.places_value(segment, enemy=True)

        segment_value = self.next_segment_values[num]  # Segment value from self.next_segment_values

        return segment.number, segment_value

    def evaluate_map_value(self, game_map):
        # Checking if game is already won or lost
        if game_map.winner:
            if game_map.winner == self.sign:
                return self.move_values["won_game"]
            elif game_map.winner == self.enemy_sign:
                return self.move_values["lost_game"]

        value = 0

        # Checking won/lost segment count
        for i in [("won_segment", self.sign), ("lost_segment", self.enemy_sign)]:
            value += self.move_values[i[0]] * self.segment_count(game_map, i[1])

        # Checking possibilities of winning/losing the game
        if self.possible_win(game_map):
            possible_wins = self.possible_win(game_map)
            value += self.move_values["possible_win"] * len(possible_wins)

        if self.possible_win(game_map, enemy=True):
            possible_defeats = self.possible_win(game_map, enemy=True)
            value += self.move_values["possible_win"] * len(possible_defeats)

        return value

    """
    Only methods that really matter
    """

    def choose_segment(self, game_map, enemy=False):
        segment_values = {str(i): 0 for i in range(1, 10)}

        # Evaluating best possible move for every segment
        for i in game_map.segments:
            # We don't want to evaluate finished segments
            if game_map.segments[i].winner:
                segment_values[i] = self.move_values["lost_game"]
            # AI/Enemy will take advantage of the situation
            elif self.possible_win(game_map, enemy) and i in self.possible_win(game_map, enemy):
                segment_values[i] = self.move_values["won_game"]
            else:
                segment_values[i] = self.pick_best_move(game_map.segments[i], game_map)[1]

        return self.return_max(segment_values)

    def pick_best_move(self, segment, game_map, enemy=False):
        # Swapping signs if evaluation is for enemy
        if enemy:
            self.sign, self.enemy_sign = self.enemy_sign, self.sign

        # Evaluates possible moves and makes copy of them
        places = copy.deepcopy(self.evaluate_all_moves(segment))

        # Clearing and rechecking possible next segments for evaluations
        self.possible_moves.clear()
        self.check_possible_moves(segment)
        segments = dict()
        maps = dict()

        for i in self.possible_moves:
            map_mirror = MapMirror(game_map, segment.number, i, self.sign)  # Evaluates segments on updated map
            map_mirror.update()  # Checking if placed sign will have any effect on the game

            # Evaluating all possible next segments
            segment_number, segment_value = self.evaluate_next_segment(map_mirror.segments[i], map_mirror)
            # Evaluating whole map value
            map_value = self.evaluate_map_value(map_mirror)

            # Updating value dictionaries
            segments[i] = segment_value
            maps[i] = map_value

        # Sum all evaluations for every segment
        sum_dict = {i: places[i] + segments[i] + maps[i] for i in self.possible_moves}

        # Re-swapping signs
        if enemy:
            self.sign, self.enemy_sign = self.enemy_sign, self.sign

        return self.return_max(sum_dict)

    """
    Multi-turn evaluation
    """

    def recursive_algorithm(self, game_map, segment, depth, enemy=False):

        if depth == 0 or game_map.winner:
            return 0

        if segment.winner:
            segment_number = self.choose_segment(game_map, enemy)[0]
            segment = game_map.segments[segment_number]

        if not enemy:
            place_number, place_value = self.pick_best_move(segment, game_map)
            map_mirror = MapMirror(game_map, segment.number, place_number, self.sign)
            next_val = self.recursive_algorithm(map_mirror, map_mirror.segments[place_number], depth - 1, enemy=True)

            return place_value + next_val
        else:
            place_number, place_value = self.pick_best_move(segment, game_map, enemy=True)
            map_mirror = MapMirror(game_map, segment.number, place_number, self.enemy_sign)
            next_val = self.recursive_algorithm(map_mirror, map_mirror.segments[place_number], depth - 1)

            return -place_value + next_val

    def pick_place_algorithm(self, game_map, segment, depth=3):
        # Best depth == 2-4
        # Checking possible moves and making copy of it
        self.check_possible_moves(segment)
        segments = copy.deepcopy(self.possible_moves)

        # Checking if there are possibilities of losing game and erasing it
        if self.possible_win(game_map, enemy=True):
            for i in segments:
                if i in self.possible_win(game_map, enemy=True):
                    segments[i] = "del"
        segments = self.clear_dict(segments)

        # If game is lost then returns random place, it doesn't matter
        if not segments:
            return self.return_max(self.possible_moves)

        # Evaluating all possible non-losing moves through recursive algorithm
        for i in segments:
            map_mirror = MapMirror(game_map, segment.number, i, self.sign)
            value = self.recursive_algorithm(map_mirror, map_mirror.segments[i], depth, enemy=True)
            segments[i] = value

        return self.return_max(segments)


class MapMirror(Map):
    def __init__(self, original_map, segment_number, place_number, sign):
        super().__init__()
        self.winner = original_map.winner
        self.segments = copy.deepcopy(original_map.segments)
        self.places = copy.deepcopy(original_map.places)

        self.segments[segment_number].places[place_number] = sign
        self.update()
