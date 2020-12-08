def load_file(file_name):
    with open(file_name) as f:
        return f.read()


def find_floor_number(directions):
    floor = 0
    for char in directions:
        if char == '(':
            floor += 1
        else:
            floor -= 1
    return floor


def find_first_basement_time(directions):
    floor = 0
    for i in range(len(directions)):
        if directions[i] == '(':
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            return i + 1


if __name__ == '__main__':
    floor_directions = load_file('input.txt')
    floor_number = find_floor_number(floor_directions)
    print('Floor: {}'.format(floor_number))
    basement_index = find_first_basement_time(floor_directions)
    print('Floor reached on character #{}'.format(basement_index))
