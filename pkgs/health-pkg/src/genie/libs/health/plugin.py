#
#   pyATS Health plugin
#

# python
import yaml
import importlib
import logging
import functools

# pyats
from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.easypy.plugins.bases import BasePlugin
from pyats.aetest.processors.decorator import ProcessorDecorator

# genie
from genie import testbed
from genie.utils import Dq
from genie.harness.datafile.loader import TriggerdatafileLoader

logger = logging.getLogger(__name__)


class HealthCheckPlugin(BasePlugin):
    '''pyATS Health Plugin'''

    # plugin name
    name = 'pyATSHealth'

    @classmethod
    def configure_parser(cls, parser, legacy_cli=False):
        '''
        plugin parser configurations

        Arguments
        ---------
            parser: main program parser to update
            legacy_cli: boolean indicating whether to support legacy args or not
        '''
        pyats_health_grp = parser.add_argument_group('pyATS Health')

        pyats_health_grp.add_argument('--health-file',
                                      dest='health_file',
                                      default=None,
                                      help='Specify health yaml file')

        return parser

    def __init__(self, *args, **kwargs):
        self.health = None
        self.health_ready = False
        super().__init__(*args, **kwargs)

    # pre-task
    def pre_task(self, task):
        # after loading health file, add all the sections/actions in health yaml
        # will be added as global context processors to pyATS job.
        # In `health.py`, `health_dispatcher` is the code of context processor.
        # It's same concept with generator-style context-processors in pyATS.
        # the code before `yield` is pre-processor, after `yield`, it's post-processor
        #
        # reference in pyATS doc : https://pubhub.devnetcloud.com/media/pyats/docs/aetest/processors.html#context-processors

        # Skip if no testbed or no health_file
        if not runtime.testbed:
            if self.runtime.args.health_file:
                # show message when testbed yaml only is missed
                logger.info('testbed yaml was not given, so pyATS health will not run')
            return

        # skip if no health_file
        if not self.runtime.args.health_file:
            return

        logger.info('Pre-Task %s: pyATS Health' % task.taskid)

        # convert from pyATS testbed to Genie testbed
        tb = testbed.load(runtime.testbed)

        # convert from pyATS testbed to Genie testbed
        loader = TriggerdatafileLoader(testbed=tb)
        with open(self.runtime.args.health_file) as f:
            health_loaded = loader.load(f.read())

        # save `pyats_health.yaml` to runtime.directory for archive
        with open(
                "{rundir}/pyats_health.yaml".format(
                    rundir=self.runtime.directory), 'w') as f:
            yaml.dump(health_loaded, f)

        # get `source` for pyATS Health processors and instantiate class
        source = health_loaded.get('pyats_health_processors',
                                   {}).get('source', {})
        if source:
            # get class name of testcase in health yaml
            pkg_name = source.get('pkg', '')
            class_name = source.get('class', '')
            class_path_list = '.'.join([pkg_name, class_name]).split('.')
            module = importlib.import_module('.'.join(class_path_list[:-1]))
            class_ = getattr(module, class_path_list[-1])
            # instantiate Health class which inherited from Blitz class
            # `health_dispacher` function from Health class will be used as processor
            health = class_()

            # get section names for pyATS Health processors
            section_names = Dq(health_loaded).get_values('test_sections')
            if section_names:
                processors = task.kwargs.setdefault('processors', {})

                # loop by health items (sections)
                for section in section_names:
                    for section_name, section_data in section.items():

                        # params for health_dispacher and pass `Steps()` as dummy.
                        params = {
                            'steps': Steps(),
                            'testbed': tb,
                            'data': section_data,
                            'name': section_name
                        }

                        method = functools.partial(health.health_dispatcher,
                                                   **params)
                        # enable processor report
                        method.__report__ = True
                        # add processors to pyATS
                        processor_decorator = ProcessorDecorator()
                        processor_method = processor_decorator.context(
                            func=method,
                            name='pyATS Health Check {section_name}'.format(
                                section_name=section_name))
                        processors.setdefault('context',
                                              []).append(processor_method)

            else:
                # Block testcase when error is found
                raise Exception("Couldn't find any 'test_sections'.")
        else:
            # Block testcase when error is found
            raise Exception(
                "Couldn't find 'pyats_health_processors' section in health.yaml."
            )


# Custom Plugin Entrypoints
health_plugin = {
    'plugins': {
        'HealthCheckPlugin:': {
            'class': HealthCheckPlugin,
            'enabled': True,
            'kwargs': {},
            'module': 'genie.libs.health.plugin',
            'name': 'HealthCheckPlugin:',
        },
    },
}