from gensim import utils
import numpy as np
from scipy.spatial.distance import euclidean

import pandas as pd
# utils
import string
import nltk
import h5py

from utils.doc2vec.model import Model
from utils.doc2vec.training_data import TrainingData

# plotting
import matplotlib.pyplot as pl

import subprocess

class FeatureExtractor:
    # Stance to one hot
    stance_to_onehot = {
        'agree': np.array([1, 0, 0, 0]),
        'disagree': np.array([0, 1, 0, 0]),
        'discuss': np.array([0, 0, 1, 0]),
        'unrelated': np.array([0, 0, 0, 1])
    }

    def __init__(self, my_model: Model, translate_table: dict):
        # Point to data, model, and translation table internally
        self.data = my_model.docs_bodies
        self.model = my_model.model
        self.translate_table = translate_table

        # Initialize headline vectors
        self.hvecs = None

        # Extract all sentence vectors
        self.svecs = {t :self.model.docvecs[t] for t in list(self.data.Tag.unique())}

    # Function to infer vector representations of headlines
    def infer_vectors_headlines(self):
        dsub = self.data[['Headline', 'Headline UID']].drop_duplicates()
        self.hvecs = {}
        for row in dsub.iterrows():
            uid = row[1]['Headline UID']
            headline = row[1]['Headline']
            hline = nltk.word_tokenize(utils.to_unicode(headline.lower().translate(self.translate_table)))
            self.hvecs[uid] = self.model.infer_vector(hline)

    # Function to potentially infer vector representations of sentences
    # WARNING: squashes svecs
    def infer_vectors_sentences(self):
        dsub = self.data[['Sentence', 'Tag']].drop_duplicates()
        self.svecs = {}
        for row in dsub.iterrows():
            tag = row[1]['Tag']
            sentence = row[1]['Sentence']
            sline = nltk.word_tokenize(utils.to_unicode(sentence.lower().translate(self.translate_table)))
            self.svecs[tag] = self.model.infer_vector(sline)

    # Calculate similiraty
    def calc_similiraty(self):
        if self.hvecs is None:
            self.infer_vectors_headlines()

        cos_sim = []
        for row in self.data.iterrows():
            svec = self.svecs[row[1]['Tag']]
            hvec = self.hvecs[row[1]['Headline UID']]
            cos_sim.append(np.dot(hvec ,svec) / np.linalg.norm(hvec) / np.linalg.norm(svec))

        self.data['Similarity'] = cos_sim

    # Calculate euclidean distance
    def calc_distance(self, data):
        if self.hvecs is None:
            self.infer_vectors_headlines()

        dist = []
        for row in self.data.iterrows():
            svec = self.svecs[row[1]['Tag']]
            hvec = self.hvecs[row[1]['Headline UID']]
            dist.append(euclidean(hvec ,svec))

        self.data['Distance'] = dist

    # Calculate translated features
    def translated_features(self):
        if self.hvecs is None:
            self.infer_vectors_headlines()

        self.features = {}
        g = self.data.groupby('Headline ID')
        for i ,j in g.groups.items():
            dsub = self.data.iloc[j].sort_values('Sentence ID')
            hvec = self.hvecs[dsub.iloc[0]['Headline UID']]

            m = []
            for row in dsub.iterrows():
                svec = self.svecs[row[1]['Tag']]
                m.append(svec)
            m = np.array(m) - hvec

            self.features[i] = m

    # Export features and targets
    def feature_target_export(self, path):
        if self.features is not None:
            # Initialize hdf5
            fh = h5py.File(path, 'w')
            for hid, feature_matrix in self.features.items():
                stance = data.loc[data['Headline ID'] == hid, 'Stance'].iloc[0]
                grp = fh.create_group(str(hid))
                grp.create_dataset('features', data=feature_matrix)
                grp.create_dataset('targets', data=self.stance_to_onehot[stance])
            fh.close()

    def feature_target_load(self, fileName):

        # Load features and targets
        print('Loading and preparing data...')
        fh = h5py.File(fileName, 'r')
        # some kind of sanity check could be implemented here
        for item in  fh.attrs.keys():
            print("item: {} + : {}".format(item, fh.attrs[item]))
        #
        X = np.array([pad(fh[str(i)]['features'].value, 10) for i in range(len(fh.keys()))])
        Y = np.array([fh[str(i)]['targets'].value for i in range(len(fh.keys()))])
        fh.close()
        return (X,Y)



if __name__ == "__main__":
    # Running a full-fledged example of feature extraction from a corpus

    # Get root git directory;
    # see http://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives
    repo_dir = subprocess.\
        Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip()\
        .decode("utf-8") # conversion to string

    # Table for translating punctuation to white spaces
    add_punct_chars = '“’—'
    translate_table = dict((ord(char), ' ') for char in string.punctuation + add_punct_chars)

    # directory for data is 'fnc-1', as established by the 'git submodule' calls
    # explained in the README
    dataset_dir = "/".join([repo_dir,  "fnc-1"])
    td = TrainingData(stances_file_name= "/".join([dataset_dir,  "train_stances.csv"]),
                      bodies_file_name="/".join([dataset_dir,  "train_bodies.csv"]),
                      translate_table=translate_table)

    print("bodies ready. Going to build and train Model now")
    # build Model and train it
    m = Model(td.bodies)
    m.train()

    print("Model trained")

    # Merge stances to article bodies
    data = td.bodies.merge(td.stances, on='Body ID')

    # Save the data
    data.to_csv('body_headline_sim.csv')

    # Load
    data = pd.read_csv('body_headline_sim.csv', index_col=None)

    # Create the feature extractor
    fext = FeatureExtractor(data)

    # Force the inference of sentences
    if 0:
        fext.infer_vectors_headlines()
        fext.infer_vectors_sentences()

    # Calculate translated features
    fext.translated_features()

    # Get a list of features sorted by headline ID from the extractor
    features = [fext.features[i] for i in sorted(fext.features.keys())]

    # Plot length distribution of feature sets in associated with each document-headline pair
    lengths = [len(i) for i in features]
    p1 = pl.hist(lengths, bins=30)



