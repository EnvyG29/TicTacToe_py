from random import randint, shuffle, randrange


class TicTacToe:
    """Игра Крестики-нолики"""

    def __init__(self):
        self._place: list = []
        self._turn = 0

        self._move_player_first = None
        self._move_player_second = None
        self._move_player_third = None
        self._move_player_fourth = None

        self._move_bot_first = None
        self._move_bot_second = None
        self._move_bot_third = None
        self._move_bot_fourth = None

        # если символы в угловой и соседней клетках
        self._angle_and_adjacent_cells = {
            (0, 1): 2, (0, 3): 6, (1, 2): 0, (2, 5): 8, (3, 6): 0, (5, 8): 2, (6, 7): 8, (7, 8): 6,
            (1, 0): 2, (3, 0): 6, (2, 1): 0, (5, 2): 8, (6, 3): 0, (8, 5): 2, (7, 6): 8, (8, 7): 6
        }

        # перехват угловой клетки
        self._recapturing_angle_cell = {
            (1, 3): 0, (1, 5): 2, (3, 7): 6, (5, 7): 8,
            (3, 1): 0, (5, 1): 2, (7, 3): 6, (7, 5): 8
        }

        # если символы в углу и противоположной средней клетке
        self._angle_and_opposite_middle_cell = {
            (0, 5): 2, (0, 7): 6, (2, 3): 0, (2, 7): 8, (1, 6): 0, (5, 6): 8, (1, 8): 2, (3, 8): 6,
            (5, 0): 2, (7, 0): 6, (3, 2): 0, (7, 2): 8, (6, 1): 0, (6, 5): 8, (8, 1): 2, (8, 3): 6
        }

        # смежные углы
        self._adjacent_angles = {
            (0, 2): 1, (0, 6): 3, (2, 8): 5, (6, 8): 7,
            (2, 0): 1, (6, 0): 3, (8, 2): 5, (8, 6): 7
        }

    def _print_place(self):
        """Вывод поля в терминал"""
        print(self._place[:3],
              self._place[3:6],
              self._place[6:], sep="\n", end="\n\n")

    def start(self):
        """Старт игры"""
        self._place = [None] * 9
        self._turn = 0
        self._print_place()
        self._player_turn()

    def _player_turn(self):
        """Ход игрока"""
        while True:
            position: int = int(input(">>> ")) - 1
            if self._place[position]:
                print("клетка занята")
            else:
                break
        if position == -1:
            return
        self._turn += 1

        match self._turn:
            case 1:
                self._move_player_first = position
            case 2:
                self._move_player_second = position
            case 3:
                self._move_player_third = position

        self._place[position] = "X"
        self._print_place()
        self._check_winner()
        self._bot_turn(self._turn)

    def _bot_turn(self, turn):
        """Ход бота"""
        match turn:
            case 1:
                self._bot_turn_1()
            case 2:
                self._bot_turn_2()
            case 3:
                self._bot_turn_3()
            case 4:
                self._bot_turn_4()

    def _bot_turn_1(self):
        """Логика первого хода"""
        print(f"turn {self._turn}")
        if self._place[4] is None:

            self._move_bot_first = 4
        else:
            pos = [0, 2, 6, 8][randint(0, 3)]
            self._move_bot_first = pos

        self._place[self._move_bot_first] = "O"
        self._print_place()
        self._player_turn()

    def _bot_turn_2(self):
        """Логика второго хода"""
        print(f"turn {self._turn}")

        # если крестик в центре поля
        if self._move_player_first == 4:

            # поставить нолик в один из оставшихся углов
            if self._move_player_second == 8 - self._move_bot_first:
                self._move_bot_in_free_random_angle()

            # перекрыть линию крестиков
            else:
                self._move_bot_second = 8 - self._move_player_second

        # если в центре будет нолик
        else:

            # если крестики напротив друг друга, поставить нолик в свободный угол
            if 8 - self._move_player_first == self._move_player_second:
                if self._move_player_first in [0, 2, 6, 8]:
                    self._move_bot_in_random_middle_cell()
                else:
                    self._move_bot_in_free_random_angle()

            # остальные действия бота
            else:
                move_player_first_and_second = self._move_player_first, self._move_player_second

                # смежные углы
                if move_player_first_and_second in self._adjacent_angles:
                    self._move_bot_second = self._adjacent_angles[move_player_first_and_second]

                # перехват угловой клетки
                elif move_player_first_and_second in self._recapturing_angle_cell:
                    self._move_bot_second = self._recapturing_angle_cell[move_player_first_and_second]

                # если символы в углу и противоположной средней клетке
                elif move_player_first_and_second in self._angle_and_opposite_middle_cell:
                    self._move_bot_second = self._angle_and_opposite_middle_cell[move_player_first_and_second]

                # если символы в угловой и соседней клетках
                else:
                    self._move_bot_second = self._angle_and_adjacent_cells[move_player_first_and_second]

        self._place[self._move_bot_second] = "O"
        self._print_place()
        self._player_turn()

    def _bot_turn_3(self):
        """Логика третьего хода"""
        print(f"turn {self._turn}")

        if self._move_player_first == 4:
            move_bot_first_and_second = self._move_bot_first, self._move_bot_second

            # смежные углы
            if move_bot_first_and_second in self._adjacent_angles:
                if self._place[self._adjacent_angles[move_bot_first_and_second]] is None:
                    self._move_bot_third = self._adjacent_angles[move_bot_first_and_second]
                else:
                    self._move_bot_third = 8 - self._move_player_third

            # угол с соседней клеткой
            elif move_bot_first_and_second in self._angle_and_adjacent_cells:
                if self._place[self._angle_and_adjacent_cells[move_bot_first_and_second]] is None:
                    self._move_bot_third = self._angle_and_adjacent_cells[move_bot_first_and_second]
                else:
                    self._move_bot_in_random_cell()

            # угол со средней клеткой противоположной стены
            else:
                if (self._move_bot_first, self._move_player_third) in self._angle_and_adjacent_cells:
                    self._move_bot_third = 8 - self._move_player_third

                elif self._place[self._angle_and_opposite_middle_cell[move_bot_first_and_second]] is None:
                    self._move_bot_third = self._angle_and_opposite_middle_cell[move_bot_first_and_second]
                else:
                    self._move_bot_in_random_cell()

        else:
            # достроить победную комбинацию
            if self._place[8 - self._move_bot_second] is None:
                self._move_bot_third = 8 - self._move_bot_second

            # если прервана линия бота
            elif self._check_triangle_x():
                self._move_bot_in_random_cell()

            # прервать линию
            else:
                move_player_first_and_third = (self._move_player_first, self._move_player_third)
                move_player_second_and_third = (self._move_player_second, self._move_player_third)
                if (move_player_first_and_third in self._angle_and_adjacent_cells and
                        self._place[self._angle_and_adjacent_cells[move_player_first_and_third]] is None):
                    self._move_bot_third = self._angle_and_adjacent_cells[move_player_first_and_third]
                elif (move_player_second_and_third in self._angle_and_adjacent_cells and
                      self._place[self._angle_and_adjacent_cells[move_player_second_and_third]] is None):
                    self._move_bot_third = self._angle_and_adjacent_cells[move_player_second_and_third]
                else:
                    self._move_bot_third = [
                        self._adjacent_angles[move_player_first_and_third],
                        self._adjacent_angles[move_player_second_and_third]
                    ][randint(0, 1)]

        self._place[self._move_bot_third] = "O"
        self._print_place()
        self._check_winner()
        self._player_turn()

    def _bot_turn_4(self):
        """Логика четвертого хода"""
        print(f"turn {self._turn}")

        if self._move_player_first == 4:
            if (self._move_bot_first, self._move_bot_third) in self._angle_and_adjacent_cells:
                if self._place[8 - self._move_player_third] is None:
                    self._move_bot_fourth = 8 - self._move_player_third
                else:
                    self._move_bot_in_random_cell()
                    self._draw()
            elif self._check_triangle_o():
                self._move_bot_in_random_cell()
                self._draw()

            else:
                self._move_bot_win()
        else:
            move_bot_second_and_third = (self._move_bot_second, self._move_bot_third)
            if move_bot_second_and_third in self._adjacent_angles and self._place[self._adjacent_angles[move_bot_second_and_third]]:
                self._move_bot_fourth = self._adjacent_angles[move_bot_second_and_third]
            elif self._place[8 - self._move_bot_third] is None:
                self._move_bot_fourth = 8 - self._move_bot_third
            else:
                self._move_bot_in_random_cell()
                self._draw()
        self._place[self._move_bot_fourth] = "O"
        self._print_place()
        self._check_winner()
        self._player_turn()

    def _move_bot_in_free_random_angle(self):
        """Бот поставит нолик в свободный случайный угол"""
        angles = [0, 2, 6, 8]
        shuffle(angles)
        for i in angles:
            if self._place[i] is None:
                self._move_bot_second = i
                break

    def _move_bot_in_random_middle_cell(self):
        """Бот ходит в случайную среднюю клетку"""
        self._move_bot_second = randrange(1, 7, 2)

    def _move_bot_in_random_cell(self):
        """Бот ходит на случайную свободную клетку"""
        lst = []
        for i in range(9):
            if self._place[i] is None:
                lst.append(i)
        match self._turn:
            case 3:
                self._move_bot_third = lst[randint(0, len(lst) - 1)]
            case 4:
                self._move_bot_fourth = lst[randint(0, len(lst) - 1)]

    def _move_bot_win(self):
        """Бот делает победный ход"""
        lst = []
        xy = (self._move_bot_first, self._move_bot_third)
        if (xy in self._adjacent_angles and self._place[self._adjacent_angles[xy]]) is None:
            lst.append(self._adjacent_angles[self._move_bot_first, self._move_bot_third])
        xy = (self._move_bot_second, self._move_bot_third)

        if xy in self._angle_and_adjacent_cells and self._place[8 - self._move_bot_first] is None:
            lst.append(self._angle_and_adjacent_cells[xy])
        shuffle(lst)

        self._move_bot_fourth = lst[randint(0, len(lst) - 1)]

    @staticmethod
    def _get_patterns_triangle() -> tuple[set[int], set[int], set[int], set[int], set[int], set[int], set[int], set[int]]:
        """Получить комбинации треугольников"""
        return (
            {0, 5, 7}, {2, 3, 7}, {2, 5, 6}, {1, 3, 8},
            {0, 5, 6}, {0, 2, 7}, {2, 3, 8}, {1, 6, 8}
        )

    def _check_triangle_x(self) -> bool:
        """Проверить наличие треугольника из Х на поле"""
        pattern = self._get_patterns_triangle()
        if {self._move_player_second, self._move_player_first, self._move_player_third} in pattern:
            return True
        return False

    def _check_triangle_o(self) -> bool:
        """Проверить наличие треугольника из О на поле"""
        pattern = self._get_patterns_triangle()
        if {self._move_bot_first, self._move_bot_second, self._move_bot_third} in pattern:
            return True
        return False

    def _check_winner(self):
        """Проверка выигрышной комбинации"""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in winning_combinations:
            if self._place[combo[0]] == self._place[combo[1]] == self._place[combo[2]] is not None:
                print(f"Winner is {self._place[combo[0]]}\n\n\n")
                self.start()

    def _draw(self):
        """Объявить ничью"""
        self._place[self._move_bot_fourth] = "O"
        self._print_place()
        print("DRAW\n\n\n")
        self.start()
