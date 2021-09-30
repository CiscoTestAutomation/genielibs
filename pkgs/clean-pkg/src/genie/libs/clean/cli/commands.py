import logging

# Genie
from genie.libs.clean.utils import validate_clean

# pyATS
from pyats.cli.base import Subcommand
from pyats.utils.commands import do_lint

log = logging.getLogger(__name__)


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
                                 type=str,
                                 help='Clean datafile to validate',
                                 required=True)
        # add testbed datafile
        self.parser.add_argument('--testbed-file',
                                 metavar='FILE',
                                 type=str,
                                 help='Testbed datafile to validate clean with',
                                 required=True)
        # enable lint
        self.parser.add_argument('--no-lint',
                                 action = 'store_false',
                                 dest = 'lint',
                                 default = True,
                                 help = "Do not lint the testbed YAML file")

    def run(self, args):
        if args.lint:
            do_lint(args.clean_file)

        validation_results = validate_clean(args.clean_file, args.testbed_file, False)

        if validation_results['warnings']:
            log.warning('\nWarning Messages')
            log.warning('----------------')
            log.warning(' - ' + '\n - '.join(validation_results['warnings']))

        if validation_results['exceptions']:
            log.error('\nExceptions')
            log.error('----------')
            for exception in validation_results['exceptions']:
                log.error(exception)

