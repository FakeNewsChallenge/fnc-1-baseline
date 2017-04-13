import subprocess
import os
import numpy as np
def get_git_root() -> str:
    """
    Gets git root of a project. If the code is not on git, returns empty string.
    """
    try:
        return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip()\
            .decode("utf-8")  # conversion to string
    except:
        return ""


def append_to_git_root(what: str, alternate_root: str) -> str:
    """
    Appends a path to git root, or to an alternate path (if this code is not running 
    on a git-controlled environment)
    :param what: a path
    :param alternate_root: a directory where to append if git root is not defined
    :return: a path
    """
    git_root = get_git_root()
    if (git_root == ''):
        return os.path.join(alternate_root, what)
    else:
        return os.path.join(git_root, what)


def pad(X, maxlen):
    """Pads with 0 or truncates a numpy array along axis 0 up to maxlen
    Args:
        X (ndarray): array to be padded or truncated
        maxlen (int): maximum length of the array
    Returns:
        ndarray: padded or truncated array
    """

    nrows = X.shape[0]
    delta = maxlen - nrows
    if delta > 0:
        padding = ((0,delta), (0,0))
        return np.pad(X, pad_width=padding, mode='constant')
    elif delta < 0:
        return X[:maxlen,:]
    else:
        return X

