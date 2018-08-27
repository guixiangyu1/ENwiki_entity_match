def read_file(filename , search_word):
    i = 0

    with open(filename) as f:

        for line in f:
            # line = line.strip()
            # word = line.split(',,,')[1]
            # vec  = line.split(' ')[1:]
            # if search_word in word:
            #     print(line)
            if search_word in line:
                i += 1
    print(i)


if __name__ == '__main__':
    read_file("data/enwiki_match.txt", "Appropriate_Match")