import re
pattern = re.compile(r'^(\d+)x(\d+)x(\d+)$')


def parse_file(file_name):
    data = []
    with open(file_name) as f:
        for line in f.readlines():
            match = re.match(pattern, line)
            data.append([int(x) for x in match.groups()])
    return data


def get_total_square_feet(sizes):
    total = 0
    for size in sizes:
        lw = 2 * size[0] * size[1]
        wh = 2 * size[1] * size[2]
        hl = 2 * size[2] * size[0]
        total += lw + wh + hl + min((lw, wh, hl)) // 2
    return total


def get_total_ribbon_length(sizes):
    total = 0
    for size in sizes:
        size.sort()
        #     perimeter of smallest side + volume of box
        total += 2 * size[0] + 2 * size[1] + size[0] * size[1] * size[2]
    return total


if __name__ == '__main__':
    box_sizes = parse_file('input.txt')
    total_square_footage = get_total_square_feet(box_sizes)
    print('Total square footage: {:,} ft^2'.format(total_square_footage))
    total_ribbon_length = get_total_ribbon_length(box_sizes)
    print('Total ribbon length: {:,} ft'.format(total_ribbon_length))
