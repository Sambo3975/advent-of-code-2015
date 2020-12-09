from hashlib import md5


def mine_advent_coin(key, zeroes=5):
    decimal = 0
    while True:
        decimal += 1
        full_key = key + str(decimal)
        hash_string = str(md5(full_key.encode()).hexdigest())
        valid = True
        for i in range(zeroes):
            if hash_string[i] != '0':
                valid = False
                break
        if valid:
            return decimal


if __name__ == '__main__':
    lowest_positive = mine_advent_coin('ckczppom')
    print('Lowest positive integer with a hash starting with 5 zeroes: {}'.format(lowest_positive))
    lowest_positive = mine_advent_coin('ckczppom', 6)
    print('Lowest positive integer with a hash starting with 6 zeroes: {}'.format(lowest_positive))
