from AI import AI
from map_template import *
from MiniMax import MiniMax, MiniMax_old


class Game:
    def __init__(self):
        self.ai = AI()
        self.game_map = Map()
        self.player_sign = None
        self.ai_sign = None
        self.turn_number = 0
        self.place_number = None
        self.current_segment = None

    def choose_sign(self):
        sign = input("Choose your sign:")
        if sign == "X":
            self.player_sign = "X"
            self.ai_sign = "O"
            self.ai.set_sign("O")
        elif sign == "O":
            self.player_sign = "O"
            self.ai_sign = "X"
            self.ai.set_sign("X")
        else:
            print("Invalid argument.")
            self.choose_sign()

    def choose_segment(self, player=False, ai=False):
        if player:
            number = input("Choose segment number:")
            while number not in list(str(123456789)) or number in self.game_map.taken_places:
                number = input("Choose other segment:")
            self.current_segment = number
        elif ai:
            self.current_segment = self.ai.choose_segment(self.game_map)[0]
            print("Enemy chose segment ", self.current_segment)

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

    def ai_pick_place_number(self):
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

    def ai_pick_place_number_old(self):
        return self.ai.pick_best_move(self.game_map.segments[self.current_segment], self.game_map)[0]

    def ai_turn(self):
        self.game_map.print()
        print("AI's turn")

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(ai=True)

        self.place_number = self.ai_pick_place_number_old()

        self.place_sign(self.current_segment, self.place_number, self.ai_sign)
        print(f"AI placed sign in segment {self.current_segment} on place {self.place_number}")

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 1

    def run(self):
        self.choose_sign()
        self.choose_segment(player=True)

        while not self.game_map.winner:
            self.player_turn()

            if self.game_map.winner:
                break

            self.ai_turn()

        print("Game winner:", self.game_map.winner)


if __name__ == "__main__":
    game = Game()
    game.run()
