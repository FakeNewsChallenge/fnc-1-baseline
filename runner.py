from utils.system import parse_params, check_version
import fnc_kfold
import fnc_random

if __name__ == "__main__":
    check_version()
    parse_params()

    print("Running RANDOM --------------------------")
    fnc_random.run_random()
    print("Running fnc_kfold --------------------------")
    fnc_kfold.run_fnc_kfold()

