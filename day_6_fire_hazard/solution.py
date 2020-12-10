import re
from numpy import full, amax, arange
from tkinter import Tk, Canvas, PhotoImage, mainloop

instruction_pattern = re.compile(r'^(?:turn )?(\w+) (\d+),(\d+) through (\d+),(\d+)$', flags=re.MULTILINE)


def parse_input(file_name):
    with open(file_name) as f:
        matches = re.findall(instruction_pattern, f.read())
    instructions = []
    for m in matches:
        instruction = m[0]
        x1 = int(m[1])
        y1 = int(m[2])
        x2 = int(m[3])
        y2 = int(m[4])
        instructions.append((instruction, x1, y1, x2, y2))
    return instructions


def execute_instructions(instructions):
    lights = full((1000, 1000), False)
    for i in instructions:
        for y in range(i[1], i[3] + 1):
            for x in range(i[2], i[4] + 1):
                if i[0] == 'on':
                    lights[y, x] = True
                elif i[0] == 'off':
                    lights[y, x] = False
                else:  # toggle
                    lights[y, x] = not lights[y, x]
    return lights


def count_lit(lights):
    count = 0
    for row in lights:
        for l in row:
            if l:
                count += 1
    return count


def execute_instructions_variable_light(instructions):
    lights = full((1000, 1000), 0)
    for i in instructions:
        for y in range(i[1], i[3] + 1):
            for x in range(i[2], i[4] + 1):
                if i[0] == 'on':
                    lights[y, x] += 1
                elif i[0] == 'off':
                    lights[y, x] = max(lights[y, x] - 1, 0)  # Must prevent negative values
                else:  # toggle
                    lights[y, x] += 2
    return lights


def get_total_brightness(lights):
    count = 0
    for row in lights:
        for l in row:
            count += l
    return count


def int_lerp(lo, hi, fact):
    fact = min(max(fact, 0), 1)  # Clamp between 0 and 1
    return (fact * hi) + ((1 - fact) * lo)


if __name__ == '__main__':
    light_instructions = parse_input('input.txt')
    while True:
        sel = ' '
        while sel not in ['1', '2', 'q']:
            sel = input('Select a part (q to quit): ')
        if sel in ['1', '2']:
            print("\nYou selected '{}'. Please wait for a few moments...\n".format(sel))
        if sel == '1':
            light_array = execute_instructions(light_instructions)
            lit = count_lit(light_array)
            print('{} lights are lit.\n'.format(lit))
        elif sel == '2':
            light_array = execute_instructions_variable_light(light_instructions)
            total_brightness = get_total_brightness(light_array)
            print('Total brightness: {}\n'.format(total_brightness))
        else:
            break

