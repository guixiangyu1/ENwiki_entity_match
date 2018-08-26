def read_file(filename , search_word):
    print(search_word)
    with open(filename) as f:
        for line in f:
            word = line.split(' ')[0]
            vec  = line.split(' ')[1:]
            if search_word == word:
                print(True)
                return
        print(False)
        return




def file2list(filename):
    with open(filename) as f:
        all_tags = []
        tags = []
        words = []
        all_words = []
        for line in f:
            line = line.strip()
            if (len(line) == 0 or line.startswith("-DOCSTART-")):
                if len(words) != 0:
                    all_words += [words]
                    all_tags  += [tags]
                    words = []
                    tags  = []
            else:
                words += [line.split(' ')[0]]
                tags  += [line.split(' ')[-1]]
        if len(words) != 0:
            all_words += [words]
            words = []
            all_tags  += [tags]
            tags  = []
    return all_words, all_tags


def get_chunk(tags):
    """

    :param tags: [O,O,B-LOC,I-LOC,O]
    :return: [(2,4)]
    """
    chunk_start = None
    entity_chunk = []

    for i, tag in enumerate(tags):
        if tag.split('-')[0] == 'O' and chunk_start is not None:
            entity_chunk += [(chunk_start, i)]

            chunk_start = None
        elif tag.split('-')[0] == 'B':
            if chunk_start is not None:
                entity_chunk += [(chunk_start, i)]

            chunk_start = i
        else:
            pass
    if chunk_start is not None:
        entity_chunk += [(chunk_start, len(tags))]


    return entity_chunk


def word_entity(words, entity_chunk):
    sentence = []

    entitys  = []
    for word in words:
        sentence.append(word.lower())
    for (entity_start, entity_end) in entity_chunk:
        for i in range(entity_start, entity_end):
            entitys.append(sentence[i])

    return entitys

def wiki_word(filename):
    words = []
    with open(filename) as f:
        for line in f:
            word = line.split(' ')[0]
            vec  = line.split(' ')[1:]
            words.append(word)
    return words

if __name__ == '__main__':
    # all_entity = []
    # all_words, all_tags = file2list("test.txt")
    #
    # for words, tags in zip(all_words, all_tags):
    #     entity_chunk = get_chunk(tags)
    #     entitys = word_entity(words, entity_chunk)
    #     all_entity += entitys
    # all_entity = set(all_entity)
    # wiki_entity = set(wiki_word("glove.6B.300d.txt"))
    #
    # entity_match = all_entity & wiki_entity
    #
    # entity_not_match = all_entity - entity_match
    # print(entity_not_match)
    #
    # print(len(entity_match), len(all_entity))
    # print(len(entity_match) / len(all_entity))

    read_file("data/WikipediaClean5Negative300Skip10.txt", "chandraratne")
    read_file("data/glove.6B.300d.txt", "chandraratne")

