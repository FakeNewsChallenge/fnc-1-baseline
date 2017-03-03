import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flag', action='store_true', default=False)  # can 'store_false' for no-xxx flags
    parser.add_argument('-r', '--reqd', required=True)
    parser.add_argument('-o', '--opt', default='fallback')
    parser.add_argument('arg', nargs='*') # use '+' for 1 or more args (instead of 0 or more)
    parsed = parser.parse_args()
    # NOTE: args with '-' have it replaced with '_'
    print('Result:',  vars(parsed))
    print('parsed.reqd:', parsed.reqd)

if __name__ == "__main__":
    main()
