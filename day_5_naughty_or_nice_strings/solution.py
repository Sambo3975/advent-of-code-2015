vowels = ('a', 'e', 'i', 'o', 'u')
naughty_substrings = ('ab', 'cd', 'pq', 'xy')


def read_file(file_name):
    with open(file_name) as f:
        return f.readlines()


def check_vowels(string):
    vowel_count = 0
    for char in string:
        if char in vowels:
            vowel_count += 1
        if vowel_count == 3:
            return True
    # print('{} - Naughty: not enough vowels.'.format(string[:-1]))
    return False


def check_double_letter(string):
    for i in range(len(string) - 1):
        if string[i] == string[i + 1]:
            return True
    # print('{} - Naughty: no double letter.'.format(string[:-1]))
    return False


def check_no_naughty_substrings(string):
    for i in range(len(string) - 1):
        if string[i:i+2] in naughty_substrings:
            return False
    return True


def check_strings(strings):
    nice_count = 0
    for x in strings:
        if check_vowels(x) and check_double_letter(x) and check_no_naughty_substrings(x):
            nice_count += 1
    return nice_count


def check_non_overlapping_repeat_pair(string):
    for i in range(len(string) - 4):
        pair = string[i:i+2]
        for j in range(i + 2, len(string) - 1):
            if string[j:j+2] == pair:
                return True
    return False


def check_sandwich(string):
    for i in range(len(string) - 2):
        if string[i] == string[i + 2]:
            return True


def check_strings_redux(strings):
    nice_count = 0
    for x in strings:
        if check_non_overlapping_repeat_pair(x) and check_sandwich(x):
            nice_count += 1
    return nice_count


def display_nice_strings(nice_count):
    if nice_count == 1:
        print('There is 1 nice string.')
    else:
        print('There are {} nice strings.'.format(nice_count))


if __name__ == '__main__':
    string_list = read_file('input.txt')
    print('First rule set: ', end='')
    nice_strings = check_strings(string_list)
    display_nice_strings(nice_strings)
    print('Second rule set: ', end='')
    nice_strings = check_strings_redux(string_list)
    display_nice_strings(nice_strings)
