import random
import time

from AI import AI
from map_template import *
from MiniMax import MiniMax, MiniMax_old
from time import sleep


class Game:
    def __init__(self, depth):
        self.ai_1 = AI()
        self.ai_2 = AI()
        self.game_map = Map()
        self.player_sign = None
        self.ai_1_sign = "O"
        self.ai_2_sign = "X"
        self.turn_number = 0
        self.place_number = None
        self.current_segment = None

        self.depth = depth

    def choose_sign(self, number):
        sign = input("Choose your sign:")
        if sign == "X":
            self.player_sign = "X"
            if number == 1:
                self.ai_1_sign = "O"
                self.ai_1.set_sign("O")
            elif number == 2:
                self.ai_2_sign = "O"
                self.ai_2.set_sign("O")
        elif sign == "O":
            self.player_sign = "O"
            if number == 1:
                self.ai_1_sign = "X"
                self.ai_1.set_sign("X")
            elif number == 2:
                self.ai_2_sign = "X"
                self.ai_2.set_sign("X")
        else:
            print("Invalid argument.")
            self.choose_sign(number)

    def choose_segment(self, player=False, ai=False, number=None):
        if player:
            number = input("Choose segment number:")
            while number not in list(str(123456789)) or number in self.game_map.taken_places:
                number = input("Choose other segment:")
            self.current_segment = number
        elif ai:
            if number == 1:
                self.current_segment = self.ai_1.choose_segment(self.game_map)[0]
            elif number == 2:
                self.current_segment = self.ai_2.choose_segment(self.game_map)[0]
            # print("Enemy chose segment ", self.current_segment)

    def place_sign(self, segment_number, place_number, sign):
        self.game_map.segments[segment_number].places[place_number] = sign
        self.game_map.update()

    def player_turn(self):
        self.game_map.print()
        print("Player's turn")
        print("You are right now in segment:", self.current_segment)

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(player=True)

        place_number = input("Choose place:")
        while place_number in self.game_map.segments[self.current_segment].taken_places:
            place_number = input("Choose different one:")
        self.place_number = place_number

        self.place_sign(self.current_segment, self.place_number, self.player_sign)

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 1

    def ai_pick_place_number_minimax(self):
        depth = 4
        if self.turn_number < 15:
            number = self.ai.pick_best_move(self.game_map.segments[self.current_segment], self.game_map)[0]
            return number
        if self.turn_number > 35:
            depth = 8
        if self.turn_number > 50:
            depth = 12

        position = (self.game_map, self.current_segment)
        alpha = self.ai.move_values["lost_game"]
        beta = self.ai.move_values["won_game"]
        path = [None] * depth

        MiniMax(self.ai, position, depth, alpha, beta, path)

        print(path)
        number = path[-1][1]

        return number

    def ai_pick_place_number(self, number):
        segment, game_map = self.game_map.segments[self.current_segment], self.game_map
        if number == 1:
            if self.turn_number < 20:
                return self.ai_1.pick_best_move(segment, game_map)[0]
            else:
                return self.ai_1.pick_place_algorithm(game_map, segment, 20)[0]
        else:
            if self.turn_number < 20:
                return self.ai_2.pick_best_move(segment, game_map)[0]
            else:
                return self.ai_2.pick_place_algorithm(game_map, segment, self.depth)[0]

    def ai_1_turn(self):
        # self.game_map.print()
        # print("AI_1's turn")

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(ai=True, number=1)

        self.place_number = self.ai_pick_place_number(1)

        self.place_sign(self.current_segment, self.place_number, self.ai_1_sign)
        # print(f"AI_1 placed sign in segment {self.current_segment} on place {self.place_number}")

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 1

    def ai_2_turn(self):
        # self.game_map.print()
        # print("AI_2's turn")

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(ai=True, number=2)

        self.place_number = self.ai_pick_place_number(2)

        self.place_sign(self.current_segment, self.place_number, self.ai_2_sign)
        # print(f"AI_2 placed sign in segment {self.current_segment} on place {self.place_number}")

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 1

    def run(self):
        self.choose_sign(2)
        self.choose_segment(player=True)

        while not self.game_map.winner:
            self.player_turn()

            if self.game_map.winner:
                break

            self.ai_2_turn()

        print("Game winner:", self.game_map.winner)

    def run_ai(self):
        self.ai_1.set_sign("O")
        self.ai_2.set_sign("X")
        self.current_segment = str(random.randint(1, 9))
        while not self.game_map.winner:
            # sleep(1)
            self.ai_1_turn()

            if self.game_map.winner:
                break

            # sleep(1)
            self.ai_2_turn()

        # self.game_map.print()
        # print("Game winner:", self.game_map.winner)
        # print("Rounds:", self.turn_number)
        return self.game_map.winner, self.turn_number


def test(games):
    for i in range(1, 8):
        wins = {
            "X": 0,
            "O": 0,
            "Draw": 0,
            "Turns": 0
        }
        game_count = 0
        while game_count < games:
            game = Game(i * 10)
            winner, turns = game.run_ai()
            wins[winner] = wins[winner] + 1
            wins["Turns"] = wins["Turns"] + turns
            game_count += 1
        for k in wins:
            wins[k] = wins[k] / games
        print("Depth", i * 10)
        print(wins)


if __name__ == "__main__":
    print("Started simulation")
    start = time.time()
    wins = {
        "X": 0,
        "O": 0,
        "Draw": 0,
        "Turns": 0
    }
    game_count = 0
    while game_count < 100:
        game = Game(26)
        winner, turns = game.run_ai()
        wins[winner] = wins[winner] + 1
        wins["Turns"] = wins["Turns"] + turns
        game_count += 1
        print(f"Progress: {game_count}%")
    for k in wins:
        wins[k] = wins[k] / 100
    finish = time.time()
    print("Simulation finished")
    print(f"Depth: O:20 vs X:26")
    print(wins)
    print("Time elapsed:", finish - start)

