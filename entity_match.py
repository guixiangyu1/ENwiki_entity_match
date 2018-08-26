from data_util import wiki_entity, overlap_distance, partof,\
            word_entity, file2list, get_chunk, entity_in_dataset
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pybktree
from Levenshtein import distance
import re


if __name__ == '__main__':
    i = 0
    word2wiki_entity = {}
    all_entity = []

    all_words, all_tags = file2list("test.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_words, all_tags = file2list("train.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_words, all_tags = file2list("valid.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_entity = set(all_entity)                        # all entity in datasets
    num2entity = wiki_entity("data/id_title_map.csv")       # all entity_wiki {index_num:word}
    entity2num = {num2entity[num]:num for num in num2entity}

    entity_in_wiki = set(num2entity.values())           # entity in wiki
    print("entity_in_wiki Done")

    for entity in entity_in_wiki:
        for word in entity.split(' '):
            if word in word2wiki_entity:
                word2wiki_entity[word] += [entity]
            else:
                word2wiki_entity[word] = [entity]
    entity_word_set = set(word2wiki_entity)



    print("entity_word_set DONE")

    entity_totally_match = all_entity & entity_in_wiki      # entity totally matched in wiki

    with open("num_entity_distance.txt", "w") as f:         # add totally matched entity to file
        for entity in entity_totally_match:
            num = entity2num[entity]
            f.write("{},,,{},,,{},,,Total_Match\n".format(entity, entity, num))

    Levenshtein_tree = pybktree.BKTree(distance, entity_in_wiki)
    print("Levenshtein_bktree Done")

    # Word_tree = pybktree.BKTree(distance, entity_word_set)
    # print("Word_tree Done")

    for entity_to_be_match in (all_entity - entity_totally_match):
        candidates = []
        with open("num_entity_distance.txt", "a") as f:
            for long_entity in entity_totally_match:
                if partof(entity_to_be_match, long_entity):
                    candidates.append(long_entity)
            if len(candidates)!=0:
                entity_matched = process.extractOne(entity_to_be_match, candidates)
                num = entity2num[entity_matched[0]]
                f.write("{},,,{},,,{},,,Abbreviation\n".format(entity_to_be_match, entity_matched, num))
            else:
                bktree_candidates = Levenshtein_tree.find(entity_to_be_match, 2)
                candidates = [candidate for (_, candidate) in bktree_candidates]
                if len(candidates)!=0:
                    entity_matched = process.extractOne(entity_to_be_match, candidates)
                    num = entity2num[entity_matched[0]]
                    f.write("{},,,{},,,{},,,Appropriate_Match\n".format(entity_to_be_match, entity_matched, num))
                else:
                    f.write("{},,,UNK,,,UNK,,,None\n".format(entity_to_be_match))
                    # for word in re.split(' |-',entity_to_be_match):
                    #     wordtree_candidates = Word_tree.find(word,0)
                    #     for (_, candidate_word) in wordtree_candidates:
                    #         candidates += word2wiki_entity[candidate_word]
                    #         # print(candidates)
                    # if len(candidates)!=0:
                    #     entity_matched = process.extractOne(entity_to_be_match.replace('-',' '), set(candidates),
                    #                                         scorer=fuzz.token_sort_ratio)
                    #     num = entity2num[entity_matched[0]]
                    #     f.write("{},,,{},,,{},,,Part_Match\n".format(entity_to_be_match, entity_matched, num))
                    # else:
                    #     f.write("{},,,UNK,,,UNK,,,None\n".format(entity_to_be_match))

        i += 1
        print(i)

