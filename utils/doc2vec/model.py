import pandas as pd
from utils.doc2vec.labeled_line_sentence import LabeledLineSentence
# gensim modules
from gensim.models import Doc2Vec
import os

from pathlib import Path

class Model:
    """Doc2Vec Model"""

    models_directory = './doc2vec_models'
    if not os.path.exists(models_directory):
        os.makedirs(models_directory)

    # ######### Private functions
    def __file_full_path__(self) -> str:
        return '{}/news_size{}.d2v'.format(self.models_directory, self.size)

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
        # labeled sentences
        self.sentences = LabeledLineSentence(docs_bodies)
        # Make the model and build the vocab
        # Internal parameters set:
        #   `workers` = use this many worker threads to train the model (=faster training with multicore machines).
        #   `dm` defines the training algorithm. By default (`dm=1`), 'distributed memory' (PV-DM) is used.
        #       Otherwise, `distributed bag of words` (PV-DBOW) is employed.
        #   `hs` = if 1 (default), hierarchical sampling will be used for model training (else set to 0).
        self.model = Doc2Vec(min_count = min_count, window = window, size = size, workers = 8, dm = 0, hs = 1)
        self.model.build_vocab(self.sentences.to_array())

    def train(self):
        """
        Trains and saves resulting model.
        :return: None
        """
        for epoch in range(20):
            self.model.train(self.sentences.sentences_perm())
        self.model.save(self.__file_full_path__())

    def load_trained(self):
        """
        Loads a trained model, if such thing exists. Trains a new one otherwise.
        :return: 
        """
        try:
            self.model = Doc2Vec.load(self.__file_full_path__())
        except FileNotFoundError:
            self.train()

    def is_trained(self)->bool:
        """
        Is there a file with a trained version?
        """
        return Path(self.__file_full_path__()).is_file()
