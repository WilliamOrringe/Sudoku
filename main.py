class Sudoku:
    def __init__(self, datum: [[]]):
        self.data = self.make_usable(datum)

    def is_solved(self):
        counts = [0 for _ in range(10)]
        for value in self.data:
            counts[value.get_value()] += 1
        if counts[0] > 0:
            return False
        for val in range(len(counts)):
            if not counts[val] == 9:
                return False
        return True

    class Value:
        def __init__(self, value, position):
            self.value = value
            self.position = position
            str_index = str(position)
            if len(str_index) < 2:
                str_index = "0" + str_index
            position = [int(str_index[0]), int(str_index[1])]
            grid = 3 * (position[0] // 3) + position[1] // 3
            self.grid = grid
            self.coords = position

        def get_value(self):
            return self.value

        def set_value(self, val):
            self.value = val

        def get_position(self):
            return self.position

        def get_grid(self):
            return self.grid

        def __repr__(self):
            return str(self.value)

    def simple_show(self):
        horizontal = "-------------------"
        print(horizontal)
        for index in range(len(self.data)):
            values = self.data[index].get_value()
            new_values = str(values) if values > 0 else "*"
            print("" + new_values + " ", end='')
            if (index + 1) % 3 == 0:
                print(" ", end='')
            if (index + 1) % 9 == 0:
                print()
            if (index + 1) % 27 == 0:
                print(horizontal)

    def make_usable(self, datum):
        new_data = []
        index = 0
        for line in datum:
            for value in line:
                new_data.append(self.Value(value, index))
                index += 1
            index += 1
        return new_data


def find_all_values(value_check: Sudoku.Value, sudok: Sudoku):
    grid_val = value_check.get_grid()
    position = value_check.coords
    stack = []
    for value in sudok.data:
        if value in stack or value.get_grid() == grid_val or position[-1] == value.coords[-1] \
                or position[0] == value.coords[0] and value.get_value() > 0:
            stack.append(value.get_value())
    real_values = []
    for i in range(1, 10):
        if i not in stack:
            real_values.append(i)
    return real_values


def recurse_solve(sudok: Sudoku, index, data_vals):
    if index == 81:
        sudok.simple_show()
        return True
    if sudok.data[index].get_value() != 0:
        return recurse_solve(sudok, index + 1, data_vals)
    choices = find_all_values(sudok.data[index], sudok)
    for choice in choices:
        sudok.data[index].set_value(choice)
        if recurse_solve(sudok, index + 1, data_vals):
            return True
        sudok.data[index].set_value(0)
    return False


if __name__ == "__main__":
    data_values = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 8, 4, 1],
                   [0, 0, 0, 6, 0, 0, 0, 7, 9], [0, 0, 8, 0, 0, 7, 4, 0, 0],
                   [0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 4, 8, 2, 9, 0, 0],
                   [0, 9, 0, 5, 0, 1, 0, 0, 0], [0, 7, 3, 0, 0, 0, 0, 2, 5],
                   [0, 1, 4, 0, 0, 0, 0, 9, 3]]
    new_l = []
    for data in data_values:
        new_l += data
    sudo = Sudoku(data_values)
    sudo.simple_show()
    recurse_solve(sudo, 0, new_l)
