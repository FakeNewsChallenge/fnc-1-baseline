import nltk

# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence

import pandas as pd

from random import shuffle

class LabeledLineSentence(object):

    columns_in_body = ['Sentence', 'Body ID', 'Sentence ID']

    def __init__(self, bodies: pd.DataFrame):
        # let's make sure we have all columns we need (instead of duck-typing our code)
        assert (set(self.columns_in_body).issubset(set(bodies.columns))), \
            "Dataframe doesn't have columns we need: {}; instead it has {}".format(", ".join(self.columns_in_body), ", ".join(bodies.columns))

        self.bodies = bodies
        # let's build the sentences' set:
        self.sentences = []
        for row in self.bodies.iterrows():
            text = row[1]['Sentence']
            bid = row[1]['Body ID']
            sid = row[1]['Sentence ID']
            name = 'body_%d_sent_%d' % (bid, sid)

            self.sentences.append(LabeledSentence(nltk.word_tokenize(utils.to_unicode(text)), [name]))


    def to_array(self):
        """
        Left here for compatibility with the original notebook
        (as originally 'sentences' would be generated here)
        TODO: do we still need it? 
        :return: sentences.
        """
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

    def __str__(self):
        return "LabeledLineSentence with {} bodies and {} sentences (total)".format(self.bodies.shape[0], len(self.sentences))