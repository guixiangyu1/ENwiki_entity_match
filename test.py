from data_util import wiki_entity, overlap_distance, partof,\
            word_entity, file2list, get_chunk, entity_in_dataset
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pybktree
from Levenshtein import distance

if __name__ == '__main__':
    i = 0
    entity2wiki = {}
    all_entity = []

    all_words, all_tags = file2list("test.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_words, all_tags = file2list("train.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_words, all_tags = file2list("valid.txt")
    all_entity += entity_in_dataset(all_words, all_tags)

    all_entity = set(all_entity)                        # all entity in datasets
    num2entity = wiki_entity("id_title_map.csv")       # all entity_wiki {index_num:word}
    entity2num = {num2entity[num]:num for num in num2entity}

    entity_in_wiki = set(num2entity.values())           # entity in wiki
    print("SET DONE")

    entity_totally_match = all_entity & entity_in_wiki      # entity totally matched in wiki

    with open("num_entity_distance.txt", "w") as f:         # add totally matched entity to file
        for entity in entity_totally_match:
            num = entity2num[entity]
            f.write("{} {} {} Total_Match\n".format(entity, entity, num))

    Levenshtein_tree = pybktree.BKTree(distance, entity_in_wiki)
    print("Levenshtein_bktree Done")

    Overlap_tree = pybktree.BKTree(overlap_distance, entity_in_wiki)
    print("Overlap_tree Done")

    for entity_to_be_match in (all_entity - entity_totally_match):
        with open("num_entity_distance.txt", "a") as f:
            for long_entity in entity_totally_match:
                if partof(entity_to_be_match, entity_totally_match):
                    candidates.append(entity_totally_match)
            if len(candidates)!=0:
                entity_matched = process.extractOne(entity_to_be_match, candidates)
                num = entity2num[entity_matched]
                f.write("{} {} {} Abbreviation".format(entity_to_be_match, entity_matched, num))
            else:
                bktree_candidates = Levenshtein_tree.find(entity_to_be_match, 1)
                candidates = [candidate for (_, candidate) in bktree_candidates]
                if len(candidates)!=0:
                    entity_matched = process.extractOne(entity_to_be_match, candidates)
                    num = entity2num[entity_matched]
                    f.write("{} {} {} Appropriate_Match".format(entity_to_be_match, entity_matched, num))
                else:
                    overlap_candidates = Overlap_tree.find(entity_to_be_match, 19)
                    candidates = [candidate for (_, candidate) in overlap_candidates]
                    if len(candidates) != 0:
                        entity_matched = process.extractOne(entity_to_be_match, candidates)
                        num = entity2num[entity_matched]
                        f.write("{} {} {} Overlap_Match".format(entity_to_be_match, entity_matched, num))
                    else:
                        f.write("{} UNK UNK None".format(entity_to_be_match))
        i += 1
        print(i)

