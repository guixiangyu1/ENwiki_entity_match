def read_file(filename , search_word):

    with open(filename) as f:
        for line in f:
            line = line.strip()
            word = line.split(',')[1]
            vec  = line.split(' ')[1:]
            if search_word in word:
                print(line)


if __name__ == '__main__':
    read_file("data/id_title_map.csv", "Taleban")