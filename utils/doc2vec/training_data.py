
import pandas as pd
import nltk
from tqdm import tqdm
import re

class TrainingData:

    def __init__(self, stances_file_name: str, bodies_file_name: str, translate_table: dict):
        # function to clean text based on dictionary
        clean_text = lambda x: re.sub("([0-9]+)((,|\.)?[0-9]*)", " ||number|| ", x.lower().translate(translate_table))

        #
        # We load the datasets from the fake news challenge into pandas data frames.
        # The article bodies are split into their component sentences. The article bodies
        # datatest thus processed is merged with the headlines and stances dataset.
        self.stances = pd.read_csv(stances_file_name)

        # Assign IDs to all headlines even if they're duplicated (almost like row numbering)
        self.stances['Headline ID'] = range(self.stances.shape[0])

        # Assign UIDs to headlines
        u_headlines = list(self.stances['Headline'].unique())
        headline_to_uid = {h: i for i, h in enumerate(u_headlines)}
        self.stances['Headline UID'] = self.stances['Headline'].map(lambda x: headline_to_uid[x])

        self.bodies = pd.read_csv(bodies_file_name)

        # Tokenize article bodies into sentences
        sentences = []
        sentence_ids = []
        body_ids = []
        for row in tqdm(self.bodies.iterrows()):
            bid = row[1]['Body ID']
            text = row[1]['articleBody']
            lines = nltk.sent_tokenize(text)
            lines = [clean_text(l) for l in lines]

            sentences += lines
            sentence_ids += range(len(lines))
            body_ids += [bid] * len(lines)

        # Create sentences dataframe and merge
        temp = pd.DataFrame({'Sentence': sentences, 'Sentence ID': sentence_ids, 'Body ID': body_ids})
        self.bodies = self.bodies.merge(temp, on='Body ID')
        self.bodies['Tag'] = 'body_' + self.bodies['Body ID'].astype(str) + '_sent_' + self.bodies['Sentence ID'].astype(str)
        # Just sort the datasets
        self.stances.sort_values(by='Body ID', inplace=True)
        self.bodies.sort_values(by='Body ID', inplace=True)
