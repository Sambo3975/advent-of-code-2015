def lerp(a, b, c):
    return int(c * a + (1 - c) * b)


class MagicMatrix:
    """A 'magic matrix' that expands infinitely in all directions'"""

    def __init__(self, empty_char='.'):
        self.__data = {}
        self.__extents = [0, 0, 0, 0]  # x1, y1, x2, y2
        self.__column_width = 1
        self.min = None
        self.max = None
        self.empty_char = empty_char

    def __getitem__(self, item):
        key = MagicMatrix.__translate_index(item)
        if key in self.__data:
            return self.__data[key]
        else:
            return None

    def __setitem__(self, key, value):
        translated_key = MagicMatrix.__translate_index(key)
        if translated_key not in self.__data:
            self.__extents[0] = min(self.__extents[0], key[0])
            self.__extents[1] = min(self.__extents[1], key[1])
            self.__extents[2] = max(self.__extents[2], key[0])
            self.__extents[3] = max(self.__extents[3], key[1])
        self.__column_width = max((self.__column_width, len(str(value)), len(str(self.__extents[0])),
                                   len(str(self.__extents[2]))))
        if self.min is None:
            self.min = value
            self.max = value
        else:
            self.min = min(self.min, value)
            self.max = max(self.max, value)
        self.__data[translated_key] = value

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        string = ''
        for i in range(self.__extents[0], self.__extents[2] + 1):
            string += '[ '
            for j in range(self.__extents[1], self.__extents[3] + 1):
                value = self[i, j]
                if value is not None:
                    string += str(value)
                    string += ' ' * (self.__column_width - len(str(value)))
                else:
                    string += self.empty_char
                    string += ' ' * (self.__column_width - 1)
                string += ' '
            string += ']  ' + str(i) + '\n' if i < self.__extents[2] else ']  ' + str(i)
        string += '\n\n  '
        for i in range(self.__extents[1], self.__extents[3] + 1):
            string += str(i)
            string += ' ' * (self.__column_width - len(str(i)) + 1)
        return string

    @staticmethod
    def __translate_index(item):
        assert isinstance(item, tuple) and len(item) == 2, 'Invalid index'
        return '{}, {}'.format(item[0], item[1])

    def get_width(self):
        return self.__extents[2] - self.__extents[0] + 1

    def get_height(self):
        return self.__extents[3] - self.__extents[1] + 1


def read_file(file_name):
    with open(file_name) as f:
        return f.read()


def give_gifts(directions):
    grid = MagicMatrix()
    x = 0
    y = 0
    grid[y, x] = 1
    for char in directions:
        if char == '^':
            y -= 1
        elif char == 'v':
            y += 1
        elif char == '<':
            x -= 1
        else:
            x += 1

        if grid[y, x] is not None:
            grid[y, x] += 1
        else:
            grid[y, x] = 1

    return len(grid), grid


def give_gifts_tandem(directions):
    grid = MagicMatrix()
    santa_x = 0
    santa_y = 0
    robo_x = 0
    robo_y = 0
    grid[santa_y, santa_x] = 2
    robo = False
    for char in directions:
        if char == '^':
            if robo:
                robo_y -= 1
            else:
                santa_y -= 1
        elif char == 'v':
            if robo:
                robo_y += 1
            else:
                santa_y += 1
        elif char == '<':
            if robo:
                robo_x -= 1
            else:
                santa_x -= 1
        else:
            if robo:
                robo_x += 1
            else:
                santa_x += 1

        x = robo_x if robo else santa_x
        y = robo_y if robo else santa_y
        if grid[y, x] is not None:
            grid[y, x] += 1
        else:
            grid[y, x] = 1

        robo = not robo

    return len(grid), grid


if __name__ == '__main__':
    gift_directions = read_file('input.txt')
    houses, house_grid = give_gifts(gift_directions)
    print('Visited {} houses. Map:'.format(houses))
    print(house_grid)
    houses, house_grid = give_gifts_tandem(gift_directions)
    print('Visited {} houses with Robo-Santa. Map:'.format(houses))
    print(house_grid)
