__author__ = "Yarik Menchaca Resendiz"
__email__ = "YarikMenchacaR@gmail.com"

import collections
from typing import Dict
import numpy as np


def NCRlexicon2dict(file_path: str) -> dict:
    with open(file_path) as file:
        emotion_dict = collections.defaultdict(list)
        for line in file.readlines():
            split_line = line.split('\t')
            if split_line[2] == '1\n':
                emotion_dict[split_line[1]].append(split_line[0])
    return emotion_dict

def lexicon_one_hot_encoding(sentence: str, lexicon:Dict[str, list])-> list:
    onehot = np.zeros(len(lexicon))
    sentence_words = set(sentence.split())
    for index, key in enumerate(lexicon):
        if sentence_words.intersection(set(lexicon[key])):
            onehot[index] = 1
    return onehot


def sentence_strength(sentence: str, lexicon: Dict[str, list]) -> list:
    emotion_words_count = collections.defaultdict(lambda: 0)
    for word in sentence.split():
        for key, value in lexicon.items():
            if word in set(value):
                emotion_words_count[key] += 1
    if emotion_words_count.values():
        return max(emotion_words_count.values())
    return 0



