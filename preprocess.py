__author__ = "Yarik Menchaca Resendiz"
__email__ = "YarikMenchacaR@gmail.com"

from xml.dom import minidom
from typing import Iterable
from pathlib import Path
from itertools import chain
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET


class EmotionStimulus:
    def __init__(self, dir_path: str):
        self._emotion_cause = Path(dir_path, 'Emotion Cause.txt')
        self._no_cause = Path(dir_path, 'No Cause.txt')
        self.sentence_tags: tuple = self.get_sentence_tags()
        self.sentences: list = [sentence for sentence, _ in self.sentence_tags]
        self.tags: list = [tag for _, tag in self.sentence_tags]
        self.emotions: set = set(self.tags)

    def get_text_and_label(self, string: str) -> tuple:
        string = string.replace("<\\", "</")
        # removing <cause> tags
        string = string.replace('<cause>', '').replace('</cause>', '')
        tree = minidom.parseString(string)
        tag = tree.childNodes[0].tagName
        text = tree.childNodes[0].firstChild.nodeValue
        return text, tag

    def get_sentence_tags(self) -> Iterable[tuple]:
        with open(self._emotion_cause) as file:
            sentence_label_cause = [self.get_text_and_label(line) for line in
                                      file.readlines()]

        sentence_label_no_cause = list()
        with open(self._no_cause) as file:
            for line in file.readlines():
                try:
                    sentence_label_no_cause.append(self.get_text_and_label(line))
                except:
                    pass
        return sentence_label_cause + sentence_label_no_cause


class DailyDialog:
    def __init__(self, dir_path: str):
        self._text = Path(dir_path, 'dialogues_text.txt')
        self._emotion = Path(dir_path, 'dialogues_emotion.txt')
        self.emotion_code = {'0': 'no emotion', '1': 'anger',
                             '2': 'disgust', '3': 'fear',
                             '4': 'happiness', '5': 'sadness', '6': 'surprise'}

        self.sentence_tags: tuple = self.get_sentence_tags()
        self.sentences: list = [sentence for sentence, _ in self.sentence_tags]
        self.tags: list = [tag for _, tag in self.sentence_tags]
        self.emotions: set = set(self.tags)

    def get_sentence_tags(self) -> Iterable[tuple]:
        with open(self._text, 'r') as file:
            text_data = [row.split('__eou__')[:-1] for row in
                         (map(str.strip, file.readlines()))]

        with open(self._emotion, 'r') as file:
            emotion_data = list(map(str.split, map(str.strip,
                                                   file.readlines())))

        text_emotion = list(zip(list(chain.from_iterable(text_data)),
                                list(self.emotion_code[emotion] for emotion in
                                     chain.from_iterable(emotion_data))))

        return text_emotion


class ISEAR:
    def __init__(self, dir_path: str):
        self.csv_file = Path(dir_path)
        self.sentence_tags: tuple = self.get_sentence_tags()
        self.sentences: list = [sentence for sentence, _ in self.sentence_tags]
        self.tags: list = [tag for _, tag in self.sentence_tags]
        self.emotions: set = set(self.tags)

    def get_sentence_tags(self) -> Iterable[tuple]:
        raw_data = pd.read_csv(self.csv_file)
        return list(raw_data[['content', 'sentiment']].to_records(index=False))


class AffectiveText:
    def __init__(self, dir_path: str):
        self._train = Path(dir_path, 'AffectiveText.test')
        self._test = Path(dir_path, 'AffectiveText.trial')
        self.sentence_tags: tuple = self.get_sentence_tags()
        self.sentences: list = [sentence for sentence, _ in self.sentence_tags]
        self.tags: list = [tag for _, tag in self.sentence_tags]
        self.emotions: set = set(self.tags)

    def get_sentence_tags(self):
        tree = ET.parse(self._train.joinpath('affectivetext_test.xml'))
        root = tree.getroot()

        with open(self._train.joinpath('affectivetext_test.emotions.gold'),
                  'r') as file:
            emotion_dict = {row[0]: row[1:] for row in
                            map(str.split, map(str.strip, file.readlines()))}

        train_data = self.generate_text_emotion_tuple(root, emotion_dict)

        # Test Data

        tree_test = ET.parse(self._test.joinpath('affectivetext_trial.xml'))
        root_test = tree_test.getroot()
        with open(self._test.joinpath('affectivetext_trial.emotions.gold'),
                  'r') as file:
            emotion_dict_test = {row[0]: row[1:] for row in map(str.split,
                                                                map(str.strip,
                                                                    file.readlines()))}

        test_data = self.generate_text_emotion_tuple(root_test,
                                                     emotion_dict_test)
        return train_data + test_data

    def generate_text_emotion_tuple(self, tree_root, emo_dict: dict) -> list:

        emotions_order = ['anger', 'disgust', 'fear', 'joy', 'sadness',
                          'surprise']
        emotion_text_tuple = list()

        for element in tree_root.findall('instance'):
            t_id = element.attrib['id']
            text = element.text
            if max(list(map(int, emo_dict[t_id]))) != 0:
                emotion = emotions_order[
                    np.argmax(list(map(int, emo_dict[t_id])))]
                emotion_text_tuple.append((text, emotion))
        return emotion_text_tuple
