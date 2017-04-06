import subprocess
import os

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

