import unittest
import feature_engineering


class FeatureEngineeringTest(unittest.TestCase):

    # Refuting Words Features
    def test_length_of_refuting_words_results(self):
        # Two parts for this test:
        # Part 1: Number of results must be equal to number of headlines:
        bunch_of_headlines = ["Headline for my news article. Pretty good stuff, I have to say", "Another headline"]
        bunch_of_bodies = ["body 1", "body 2"]
        r = feature_engineering.refuting_features(bunch_of_headlines, bunch_of_bodies)
        self.assertEqual(len(r), len(bunch_of_headlines))
        # Part 2: OK, we have one list per headline. Now: what is the size of each line of those list?
        # Should be == number of refuting words.
        all_lengths = list(map(len, r))
        self.assertTrue(
            all(map(lambda a_length: a_length == len(feature_engineering._refuting_words), all_lengths)),
            'all lengths = {}'.format(all_lengths)
        )

    def test_refuting_words_in_headline(self):
        # if I have a sentence with only refuting words, then I only get 0's
        all_refuting_headline = " ".join(feature_engineering._refuting_words)
        a_body = all_refuting_headline # doesn't matter, really
        r = feature_engineering.refuting_features([all_refuting_headline], [a_body])
        self.assertEqual(len(r), 1)
        self.assertTrue(0 not in r[0], 'There are 1s in a full refuted sentence: {} with sentence \"{}\"'.format(r, all_refuting_headline))

    def test_other(self):
        # if I have a sentence with NO refuting words, then I should get only 0's
        # How may 0's? == number of refuting words.
        a_headline = "Headline for my news article. Pretty good stuff, I have to say"
        # sanity check: does my sentence contain any refuting word. If it does. explode:
        a_headline_as_list = a_headline.split()
        self.assertTrue(len(list(set(a_headline_as_list) & set(feature_engineering._refuting_words))) == 0)
        # ok, pretty good. Let's do it:
        a_body = a_headline # doesn't matter, really
        r = feature_engineering.refuting_features([a_headline], [a_body])
        self.assertEqual(len(r), 1)
        # print(r)
        self.assertTrue(1 not in r[0])

if __name__ == '__main__':
    unittest.main()