from fuzzywuzzy import fuzz
from Levenshtein import distance


def read_file(filename , search_word):
    indicate=False
    with open(filename) as f:
        for line in f:
            line = line.strip()
            word = line.split(',')[1]
            # vec  = line.split(' ')[1:]
            # if search_word in word:
            #     print(line)
            if search_word == word:
                indicate = True
    print(search_word, indicate)
    return indicate
def wiki_entity(filename):
    entity2vec = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("ENTITY/"):
                line = line.replace("ENTITY/"," ").strip()
                if len(line)!=0:
                    word = line.split(' ')[0]

                    vec = [float(x) for x in line.split(' ')[1:]]

                    word = word.replace('_',' ').title()

                    entity2vec[word] = vec
    return  entity2vec
            # vec  = line.split(' ')[1:]
            # if search_word in word:
            #     print(line)
            # if search_word == word:
            #     indicate = True

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
    entity   = ""
    entitys  = []
    for word in words:
        sentence.append(word.lower())
    for (entity_start, entity_end) in entity_chunk:
        for i in range(entity_start, entity_end):
            entity = entity + sentence[i] + " "
        entity = entity.strip()
        entitys.append(entity)
        entity = ""
    return entitys

def entity_in_dataset(all_words, all_tags):
    all_entity = []
    for words, tags in zip(all_words, all_tags):
        entity_chunk = get_chunk(tags)
        entitys = word_entity(words, entity_chunk)
        all_entity += entitys
    all_entity = set(all_entity)
    return all_entity

def partial_ratio(x,y):
    return 100 - fuzz.partial_ratio(x,y)

def overlap_distance(s1,s2):
    s1_words = set(s1.split(' '))
    s2_words = set(s2.split(' '))
    return 20-len(s2_words&s1_words)

def partof(s1,s2):
    indicate = True
    s1_words = set(s1.split(' '))
    s2_words = set(s2.split(' '))
    for s1_word in s1_words:
        if s1_word not in s2_words:
            indicate = False
            break
    return indicate




    # entity_match = all_entity & wiki_entity
    # print(len(entity_match), len(all_entity))
    # print(len(entity_match)/len(all_entity))
    # print(all_entity - entity_match)

    # entity_match, entity_total = 0., 0.
    # for i in all_entity:
    #     for j in wiki_entity:
    #         if i in j:
    #             entity_match += 1
    #     entity_total += 1
    #     print(entity_total)
    # print(entity_match, entity_total)
    # print(entity_match/entity_total)


        # for entity in set(entitys):
        #     entity_total += 1
        #     if read_file("id_title_map.csv", entity):
        #         entity_match += 1
    # print(entity_match, entity_total)





