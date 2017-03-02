import sys
import os
import re

# supposed to work on windows
def parse_params():
    if not "--clear-cache" in sys.argv:
        return

    dry_run = "--dry-run" in sys.argv
    dr = "features"
    for f in os.listdir(dr):
        if re.search('\.npy$', f):
            fname = os.path.join(dr, f)
            if dry_run:
                print("Will delete {0}".format(fname))
            else:
                os.remove(fname)
    for f in ['hold_out_ids.txt', 'training_ids.txt']:
        fname = os.path.join('splits', f)
        if os.path.isfile(fname):
            if dry_run:
                print("Will delete {0}".format(fname))
            else:
                os.remove(fname)
    print("All clear")
    sys.exit(0)

def check_version():
    if sys.version_info.major < 3:
        sys.stderr.write('Please use Python version 3 and above\n')
        sys.exit(1)
