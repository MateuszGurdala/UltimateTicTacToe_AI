class Segment:
    def __init__(self, number):
        self.number = number
        self.winner = None
        self.taken_places = set()
        self.places = {str(i): None for i in range(1, 10)}

    # Checking every possible combination to decide if segment is finished
    def check_rows(self):
        sp = self.places
        for i in range(3):
            row = [sp[str(1 + 3 * i)], sp[str(2 + 3 * i)], sp[str(3 + 3 * i)]]
            if row in [["X", "X", "X"], ["O", "O", "O"]]:
                if row == ["X", "X", "X"]:
                    self.winner = "X"
                else:
                    self.winner = "O"

    def check_columns(self):
        sp = self.places
        for i in range(3):
            row = [sp[str(1 + i)], sp[str(4 + i)], sp[str(7 + i)]]
            if row in [["X", "X", "X"], ["O", "O", "O"]]:
                if row == ["X", "X", "X"]:
                    self.winner = "X"
                else:
                    self.winner = "O"

    def check_diagonals(self):
        sp = self.places
        for i in range(2):
            row = [sp[str(1 + 6 * i)], sp[str(5)], sp[str(9 - 6 * i)]]
            if row in [["X", "X", "X"], ["O", "O", "O"]]:
                if row == ["X", "X", "X"]:
                    self.winner = "X"
                else:
                    self.winner = "O"

    def check_if_won(self):
        self.check_rows()
        self.check_columns()
        self.check_diagonals()

        if len(self.taken_places) == 9 and not self.winner:
            self.winner = "Draw"

        if self.winner:
            return True
        return False

    def update(self):
        for i in self.places:
            if self.places[i]:
                self.taken_places.add(i)

        self.check_if_won()


class Map(Segment):
    def __init__(self):
        super().__init__(number=0)
        self.segments = {str(i): Segment(str(i)) for i in range(1, 10)}

    def update(self):
        for i in self.segments:
            self.segments[i].update()
            if self.segments[i].winner:
                self.taken_places.add(i)
                self.places[i] = self.segments[i].winner

        if self.check_if_won():
            return True

    def print(self):
        gp = self.places
        for i in range(1, 10):
            gsp = self.segments[str(i)].places
            for j in range(1, 10):
                if not gsp[str(j)]:
                    gsp[str(j)] = " "
                if not gp[str(j)]:
                    gp[str(j)] = " "

        for i in range(3):
            sp_1 = self.segments[str(1 + 3 * i)].places
            sp_2 = self.segments[str(2 + 3 * i)].places
            sp_3 = self.segments[str(3 + 3 * i)].places
            for k in range(3):
                print(sp_1[str(1 + 3 * k)], sp_1[str(2 + 3 * k)], sp_1[str(3 + 3 * k)], "|",
                      sp_2[str(1 + 3 * k)], sp_2[str(2 + 3 * k)], sp_2[str(3 + 3 * k)], "|",
                      sp_3[str(1 + 3 * k)], sp_3[str(2 + 3 * k)], sp_3[str(3 + 3 * k)], "|", )
            print("=" * 23)

        for k in range(3):
            print(gp[str(1 + 3 * k)], "|", gp[str(2 + 3 * k)], "|", gp[str(3 + 3 * k)])

        for i in range(1, 10):
            gp = self.places
            gsp = self.segments[str(i)].places
            for j in range(1, 10):
                if gsp[str(j)] == " ":
                    gsp[str(j)] = None
                if gp[str(j)] == " ":
                    gp[str(j)] = None
