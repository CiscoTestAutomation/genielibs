import logging
import argparse

# Genie
from genie.libs.clean.utils import validate_schema

# pyATS
from pyats.cli.base import Subcommand, ERROR
from pyats.utils.yaml import Loader
from pyats.utils.commands import do_lint

logger = logging.getLogger(__name__)


class ValidateClean(Subcommand):
    '''
    Validates that a clean datafile has the correct syntax
    '''

    name = 'clean'
    help = 'validate your clean datafile syntax'

    usage = '{prog} [options]'

    description = 'Validates the provided clean datafile for syntax and ' \
                  'content completeness.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add clean datafile
        self.parser.add_argument('--clean-file',
                                 metavar='FILE',
                                 type=argparse.FileType('r'),
                                 help='Clean datafile to validate',
                                 required=True)
        # add testbed datafile
        self.parser.add_argument('--testbed-file',
                                 metavar='FILE',
                                 type=argparse.FileType('r'),
                                 help='Testbed datafile to validate clean with',
                                 required=True)
        # enable lint
        self.parser.add_argument('--no-lint',
                                 action = 'store_false',
                                 dest = 'lint',
                                 default = True,
                                 help = "Do not lint the testbed YAML file")

    def run(self, args):
        loader = Loader(enable_extensions=True)

        try:
            logger.info('-'*70)
            logger.info('Loading clean datafile: %s' % args.clean_file.name)
            clean = loader.load(args.clean_file)

            logger.info('Loading testbed datafile: %s' % args.testbed_file.name)
            testbed = loader.load(args.testbed_file)
            logger.info('-'*70)
        except Exception as e:
            logger.error(str(e))
            return ERROR

        if args.lint:
            do_lint(args.clean_file.name)

        validate_schema(clean, testbed)
