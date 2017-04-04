from utils.system import parse_params, check_version
from utils.dataset import DataSet
import random
from utils.score import report_score, LABELS

def run_random():
    """
    Really silly predictor - knows nothing about nothing.
    :return: None
    """
    d = DataSet()
    all_instances = list(map(lambda stance: stance['Stance'], d.stances))
    unique_instances = list(set(all_instances))

    y = []
    for stance in random.sample(d.stances, int(len(d.stances) / 10)):
        y.append(LABELS.index(stance['Stance']))

    predicted = [random.choice(unique_instances) for _ in range(len(y))]
    actual = [LABELS[int(a)] for a in y]

    report_score(actual,predicted)


if __name__ == "__main__":
    check_version()
    parse_params()

    run_random()
