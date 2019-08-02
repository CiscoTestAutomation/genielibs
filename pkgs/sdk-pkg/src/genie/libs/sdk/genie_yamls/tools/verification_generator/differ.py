import yaml
import argparse
from genie.utils.diff import Diff

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-original',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='File containing original information')

    parser.add_argument('-new',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='File containing original information')
    custom_args = parser.parse_known_args()[0]

    with open(custom_args.original, 'r') as f:
        original = f.read()

    with open(custom_args.new, 'r') as f:
        new = f.read()

    new = yaml.safe_load(new)
    original = yaml.safe_load(original)

    diff = Diff(original, new)
    diff.findDiff()
    print(diff)


