import pandas as pd
from utils.doc2vec.labeled_line_sentence import LabeledLineSentence
# gensim modules
from gensim.models import Doc2Vec
import os

from pathlib import Path
from utils.Utils import append_to_git_root
import hashlib
import pickle

from typing import List

class Model:
    """Doc2Vec Model"""

    models_directory = append_to_git_root(what = './doc2vec_models', alternate_root=".")
    params_file_name = 'params.pickle'
    model_file_name = 'news.d2v'

    if not os.path.exists(models_directory):
        os.makedirs(models_directory)


    def trained_model_exists(docs_bodies: pd.DataFrame) -> bool:
        return False

    # ######### Private functions
    def __ensure_directory_exists__(self):
        d = self.persistence_directory()
        if not os.path.exists(d):
            os.makedirs(d)

    def __file_full_path__(self, filename: str) -> str:
        return '{}/{}'.format(self.persistence_directory(), filename)

    def __save__(self) -> bool:
        try:
            self.__ensure_directory_exists__()
            # Parameters
            with open(self.__file_full_path__(self.params_file_name), 'wb') as f:
                pickle.dump([self.window, self.min_count, self.size], f)
            # Doc2Vec model
            self.model.save(self.__file_full_path__(self.model_file_name))
            print("Model saved in directory '{}'".format(self.persistence_directory()))
            return True
        except:
            print("Model COULD NOT be saved in directory '{}'".format(self.persistence_directory()))
            return False


    def __load__(self) -> bool:
        try:
            # Parameters
            with open(self.__file_full_path__(self.params_file_name), 'rb') as f:
                self.window, self.min_count, self.size = pickle.load(f)
            # Doc2Vec model
            self.model = Doc2Vec.load(self.__file_full_path__(self.model_file_name))
            return True
        except:
            # whatever the reason, this didn't work, so - whatever!
            return False

    # #########

    def __init__(self, docs_bodies: pd.DataFrame, window: int = 10, min_count: int = 2, size: int = 200):
        """
        :param window is the maximum distance between the predicted word and context words used for prediction
        within a document.
        :param min_count = ignore all words with total frequency lower than this.
        :param size is the dimensionality of the feature vectors.
        """
        self.window = window
        self.min_count = min_count
        self.size = size
        self.docs_bodies = docs_bodies
        # labeled sentences
        self.sentences = LabeledLineSentence(docs_bodies)
        # let's try to load the model - in case I already trained with this corpus:
        self.__load__()

    def persistence_directory(self) -> str:
        """
        Directory where this Model should be saved.
        """
        sentences_as_strings = self.sentences.to_array()

        sentences_as_strings = list(map(str, self.sentences.to_array())) # .sort()
        sentences_as_strings.sort()
        #
        sentences_in_bodies = " ".join(sentences_as_strings)
        hash_for_sentences = hashlib.sha1(sentences_in_bodies.encode()).hexdigest()
        params_as_str = "w{}_mc{}_s{}".format(self.window, self.min_count, self.size)
        return "/".join([self.models_directory, hash_for_sentences, params_as_str])

    def train(self, window: int = 10, min_count: int = 2, size: int = 200, force: bool = False):
        """
        :param window is the maximum distance between the predicted word and context words used for prediction
        within a document.
        :param min_count = ignore all words with total frequency lower than this.
        :param size is the dimensionality of the feature vectors.
        """
        self.window = window
        self.min_count = min_count
        self.size = size
        if force or (not self.__load__()): # if I can load it, it means nothing has changed - so why train again?
            # Make the model and build the vocab
            # Internal parameters set:
            #   `workers` = use this many worker threads to train the model (=faster training with multicore machines).
            #   `dm` defines the training algorithm. By default (`dm=1`), 'distributed memory' (PV-DM) is used.
            #       Otherwise, `distributed bag of words` (PV-DBOW) is employed.
            #   `hs` = if 1 (default), hierarchical sampling will be used for model training (else set to 0).
            self.model = Doc2Vec(min_count = min_count, window = window, size = size, workers = 8, dm = 0, hs = 1)
            self.model.build_vocab(self.sentences.to_array())
            # OK, good to train!
            for epoch in range(20):
                self.model.train(self.sentences.sentences_perm())
            # and let's save - phew!
            self.__save__()

    def is_trained(self)->bool:
        """
        Is there a file with a trained version?
        """
        return Path(self.__file_full_path__(self.model_file_name)).is_file() \
               and \
               Path(self.__file_full_path__(self.params_file_name)).is_file()
