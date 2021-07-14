__author__ = "Yarik Menchaca Resendiz"
__email__ = "YarikMenchacaR@gmail.com"

from xml.dom import minidom
from typing import Iterable
from pathlib import Path
from itertools import chain
import pandas as pd


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
