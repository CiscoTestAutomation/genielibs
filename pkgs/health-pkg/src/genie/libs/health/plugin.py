#
#   pyATS Health plugin
#

# python
import re
import ast
import yaml
import json
import importlib
import logging
import functools

# pyats
from pyats.easypy import runtime
from pyats.easypy.plugins.bases import BasePlugin
from pyats.aetest.processors.decorator import ProcessorDecorator
from pyats import configuration as cfg
from pyats.utils import parser as argparse
from pyats.utils.yaml.dumper import OrderedSafeDumper

# genie
from genie import testbed
from genie.utils import Dq
from genie.harness.datafile.loader import TriggerdatafileLoader
from genie.libs.health import health_yamls

logger = logging.getLogger(__name__)

MESSAGE_URL = 'https://api.ciscospark.com/v1/messages'

MESSAGE_TEMPLATE = """
## pyATS Health Check Failure Notification
```
Device        : {device_name}
Health Name   : {health_name}
Health Type   : {health_type}
Health Result : {health_result}
Health Value  : {health_value}

Job ID        : {jobid}
Host          : {host} ({host_os})
pyATS Env     : {python_env} / pyATS {pyats_ver} / Python {python_ver}
Full-ID       : {fullid}
Testbed       : {testbed_name}
Start Time    : {starttime}
Stop Time     : {stoptime}
```
"""

try:
    from genie.libs.cisco.telemetry import add_health_usage_data
    INTERNAL = True
except:
    INTERNAL = False


class HealthCheckPlugin(BasePlugin):
    '''pyATS Health Plugin'''

    # plugin name
    name = 'pyATSHealth'
    parameters = {}

    @classmethod
    def configure_parser(cls, parser, legacy_cli=True):
        '''
        plugin parser configurations

        Arguments
        ---------
            parser: main program parser to update
            legacy_cli: boolean indicating whether to support legacy args or not
        '''
        pyats_health_grp = parser.add_argument_group('pyATS Health')

        if legacy_cli:
            health_file = ['-health_file']
            health_sections = ['-health_sections']  # deprecated
            health_tc_sections = ['-health_tc_sections']
            health_uids = ['-health_uids']  # deprecated
            health_tc_uids = ['-health_tc_uids']
            health_groups = ['-health_groups']  # deprecated
            health_tc_groups = ['-health_tc_groups']
            health_config = ['-health_config']
            health_remote_device = ['-health_remote_device']
            health_mgmt_vrf = ['-health_mgmt_vrf']
            health_threshold = ['-health_threshold']
            health_show_logging_keywords = ['-health_show_logging_keywords']
            health_clear_logging = ['-health_clear_logging']
            health_core_default_dir = ['-health_core_default_dir']
            health_checks = ['-health_checks']
            health_devices = ['-health_devices']
            health_webex = ['-health_webex']  # deprecated
            health_notify_webex = ['-health_notify_webex']
        else:
            health_file = ['--health-file']
            health_sections = ['--health-sections']  # deprecated
            health_tc_sections = ['--health-tc-sections']
            health_uids = ['--health-uids']  # deprecated
            health_tc_uids = ['--health-tc-uids']
            health_groups = ['--health-groups']  # deprecated
            health_tc_groups = ['--health-tc-groups']
            health_config = ['--health-config']
            health_remote_device = ['--health-remote-device']
            health_mgmt_vrf = ['--health-mgmt-vrf']
            health_threshold = ['--health-threshold']
            health_show_logging_keywords = ['--health-show-logging-keywords']
            health_clear_logging = ['--health-clear-logging']
            health_core_default_dir = ['--health-core-default-dir']
            health_checks = ['--health-checks']
            health_devices = ['--health-devices']
            health_webex = ['--health-webex']  # deprecated
            health_notify_webex = ['--health-notify-webex']

        pyats_health_grp.add_argument(*health_file,
                                      dest='health_file',
                                      default=None,
                                      help='Specify health yaml file')

        # DEPRECATED
        pyats_health_grp.add_argument(*health_sections,
                                      dest='health_sections',
                                      default=None,
                                      help=argparse.SUPPRESS)

        pyats_health_grp.add_argument(
            *health_tc_sections,
            dest='health_tc_sections',
            default=None,
            help='Specify sections where to run pyATS Health Check. '
                 'Regex is supported. '
                 'You can also filter based on class type. e.g. '
                 ' type:TestCase'
        )

        # DEPRECATED
        pyats_health_grp.add_argument(*health_uids,
                                      dest='health_uids',
                                      default=None,
                                      help=argparse.SUPPRESS)

        pyats_health_grp.add_argument(
            *health_tc_uids,
            dest='health_tc_uids',
            default=None,
            help='Specify triggers uids where to run pyATS Health Check. '
                 'Regex is supported'
        )

        # DEPRECATED
        pyats_health_grp.add_argument(*health_groups,
                                      dest='health_groups',
                                      default=None,
                                      help=argparse.SUPPRESS)

        pyats_health_grp.add_argument(
            *health_tc_groups,
            dest='health_tc_groups',
            default=None,
            help='Specify groups where to run pyATS Health Check. '
                 'Regex is supported'
        )

        pyats_health_grp.add_argument(
            *health_config,
            dest='health_config',
            default=None,
            help='Specify pyATS Health Check configuration yaml file')

        pyats_health_grp.add_argument(
            *health_remote_device,
            dest='health_remote_device',
            default=None,
            nargs='*',
            help='Specify remote device information for copy files to remote')

        pyats_health_grp.add_argument(
            *health_mgmt_vrf,
            dest='health_mgmt_vrf',
            default=None,
            nargs='*',
            help='Specify Mgmt Vrf which is reachable to remote device')

        pyats_health_grp.add_argument(
            *health_threshold,
            dest='health_threshold',
            default=None,
            nargs='*',
            help='Specify threshold for cpu, memory')

        pyats_health_grp.add_argument(
            *health_show_logging_keywords,
            dest='health_show_logging_keywords',
            default=None,
            nargs='*',
            help='Specify logging keywords to search')

        pyats_health_grp.add_argument(
            *health_clear_logging,
            dest='health_clear_logging',
            default=False,
            action='store_true',
            help='Specify logging keywords to search')

        pyats_health_grp.add_argument(
            *health_core_default_dir,
            dest='health_core_default_dir',
            default=None,
            nargs='*',
            help='Specify directories where to search for core files')

        pyats_health_grp.add_argument(*health_checks,
                                      dest='health_checks',
                                      default=None,
                                      nargs='*',
                                      help='Specify checks to run')

        pyats_health_grp.add_argument(
            *health_devices,
            dest='health_devices',
            default=None,
            nargs='*',
            help='Specify devices which checks run against')

        # DEPRECATED
        pyats_health_grp.add_argument(*health_webex,
                                      dest='health_webex',
                                      default=False,
                                      action='store_true',
                                      help=argparse.SUPPRESS)

        pyats_health_grp.add_argument(*health_notify_webex,
                                      dest='health_notify_webex',
                                      default=False,
                                      action='store_true',
                                      help='Flag to send webex notification')

        return parser

    def __init__(self, *args, **kwargs):
        self.health = None
        self.health_ready = False
        super().__init__(*args, **kwargs)

    # pre-task
    def pre_task(self, task):

        # warnings for deprecated arguments
        if self.runtime.args.health_sections:
            logger.warning(
                'DeprecationWarning: --health-sections is deprecated in 21.6. Use --health-tc-sections'
            )
        if self.runtime.args.health_uids:
            logger.warning(
                'DeprecationWarning: --health-uids is deprecated in 21.6. Use --health-tc-uids'
            )
        if self.runtime.args.health_groups:
            logger.warning(
                'DeprecationWarning: --health-groups is deprecated in 21.6. Use --health-tc-groups'
            )
        if self.runtime.args.health_webex:
            logger.warning(
                'DeprecationWarning: --health-webex is deprecated in 21.7. Use --health-notify-webex'
            )

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
                logger.warning(
                    'testbed yaml was not given, so pyATS health will not run')
            return

        # check if any health arguments are given without --health-file or --health-checks
        if not self.runtime.args.health_file and not self.runtime.args.health_checks:
            webex_args_list = [
                x for x in dir(self.runtime.args) if 'health' in x
            ]
            webex_args_value_list = []
            for arg in webex_args_list:
                webex_args_value_list.append(getattr(self.runtime.args, arg))
            if any(webex_args_value_list):
                raise Exception(
                    'pyATS Health Check arguments were given, but mandatory --health-file or --health-checks is missed.'
                )
            else:
                return

        logger.info('Pre-Task %s: pyATS Health' % task.taskid)

        # load health configuration
        with open(self.runtime.args.health_config
                  or health_yamls.health_config) as f:
            health_config = yaml.safe_load(f)

        if health_config:
            runtime.health_results = runtime.synchro.dict()
            runtime.health_results.update(health_config)
            runtime.health_results['health_data'] = []

        # convert from pyATS testbed to Genie testbed
        tb = testbed.load(runtime.testbed)

        # convert from pyATS testbed to Genie testbed
        loader = TriggerdatafileLoader(testbed=tb)

        # load pyats health file
        health_loaded = None
        # load via --health-file
        if self.runtime.args.health_file:
            health_loaded = loader.load(self.runtime.args.health_file)
        # load default template via --health-checks
        if self.runtime.args.health_checks and not health_loaded:
            with open(health_yamls.pyats_health_yaml) as f:
                health_loaded = loader.load(f.read())

        # get `source` for pyATS Health processors and instantiate class
        source = health_loaded.get('pyats_health_processors',
                                   {}).get('source', {})

        # check `reconnect` flag/parameters
        if 'reconnect' in health_loaded.setdefault('pyats_health_processors',
                                                   {}):
            reconnect = health_loaded['pyats_health_processors']['reconnect']
            if reconnect is None:
                # `reconnect` in yaml, but no params. pass empty dict
                reconnect = {}
        else:
            reconnect = None

        # check `health_settings` flag/parameters from health yaml
        if 'health_settings' in health_loaded.setdefault(
                'pyats_health_processors', {}):
            health_settings = health_loaded['pyats_health_processors'][
                'health_settings']
            if health_settings is None:
                # `reconnect` in yaml, but no params. pass empty dict
                health_settings = {}
        else:
            health_settings = {}

        def _evaluate_arguments(arg, variable, setting_name, exception_msg):
            checks_list = []
            devices_list = []

            if isinstance(arg, bool):
                variable[setting_name] = arg
                return

            # support both nargs and non-nargs
            for each_arg in arg if isinstance(arg, list) else [arg]:
                # support delimiter ',' instead of ' '(space) as well
                for item in re.split(r',(?![^\[]*[\]])', each_arg):
                    if len(re.split(r':(?![^\[]*[\]])', item)) != 2:
                        # healch_chckes
                        if setting_name == 'checks':
                            checks_list.append(item)
                            continue
                        # health_devices
                        elif setting_name == 'devices':
                            devices_list.append(item)
                            continue
                        else:
                            raise Exception(exception_msg)
                    k, v = re.split(r':(?![^\[]*[\]])', item)
                    if not k or not v:
                        # error out in case improper format given like `nxos:` or `nxos`
                        # which is not key and value pair
                        raise Exception(exception_msg)
                    try:
                        # change string to appropriate type
                        v = ast.literal_eval(v)
                    except Exception:
                        pass
                    variable.setdefault(setting_name, {})[k] = v
            # single value to pair. eg. cpu -> cpu: True
            if checks_list:
                for check in variable.get('checks', []):
                    variable['checks'][check] = check in checks_list
            # single value to pair. eg. R3_nx -> R3_nx: nxos
            if devices_list:
                for device in devices_list:
                    variable.setdefault(
                        'devices',
                        {})[device] = runtime.testbed.devices[device].os

        # overwrite health_settings if health args are given to pyats command
        if self.runtime.args.health_remote_device:
            _evaluate_arguments(
                self.runtime.args.health_remote_device,
                health_settings,
                'remote_device',
                exception_msg=
                'Wrong format was given to `--health-remote-device`. Format would be `name:jump_host path:/tmp via:scp`.'
            )
        if self.runtime.args.health_mgmt_vrf:
            _evaluate_arguments(
                self.runtime.args.health_mgmt_vrf,
                health_settings,
                'mgmt_vrf',
                exception_msg=
                'Wrong format was given to `--health-mgmt-vrf`. Format would be `iosxe:Mgmt-intf iosxr:None,nxos:management`.'
            )
        if self.runtime.args.health_threshold:
            _evaluate_arguments(
                self.runtime.args.health_threshold,
                health_settings,
                'threshold',
                exception_msg=
                'Wrong format was given to `--health-threshold`. Format would be `cpu:90 memory:90`.'
            )
        if self.runtime.args.health_show_logging_keywords:
            _evaluate_arguments(
                self.runtime.args.health_show_logging_keywords,
                health_settings,
                'show_logging_keywords',
                exception_msg=
                "Wrong format was given to `--health-show-logging-keywords`. Format would be `\"iosxe:['traceback','Traceback']\" \"iosxr:['TRACEBACK']\"`."
            )

        _evaluate_arguments(
            self.runtime.args.health_clear_logging,
            health_settings,
            'clear_logging',
            exception_msg=
            "Wrong format was given to `--clear-logging`. No value required. This is flag. If provide, True(clear logging)."
        )

        if self.runtime.args.health_core_default_dir:
            _evaluate_arguments(
                self.runtime.args.health_core_default_dir,
                health_settings,
                'core_default_dir',
                exception_msg=
                "Wrong format was given to `--health-core-default-dir`. Format would be `\"iosxe:['bootflash:/core/'','harddisk:/core/']\" \"iosxr:['/misc/scratch/core']\"`."
            )

        if self.runtime.args.health_checks:
            _evaluate_arguments(
                self.runtime.args.health_checks,
                health_settings,
                'checks',
                exception_msg=
                "Wrong format was given to `--health-checks`. Format would be `cpu memory`."
            )

        if self.runtime.args.health_devices:
            _evaluate_arguments(
                self.runtime.args.health_devices,
                health_settings,
                'devices',
                exception_msg=
                "Wrong format was given to `--health-devices`. Format would be R1_xe:iosxe,R2_xr:iosxr,R3_nx:nxos`."
            )

        # DEPRECATED. keep for backward compatibility
        _evaluate_arguments(
            self.runtime.args.health_webex,
            health_settings,
            'webex',
            exception_msg=
            "(DEPRECATED. PLEASE USE --health-notify-webex which is equivalent)"
        )

        _evaluate_arguments(
            self.runtime.args.health_notify_webex,
            health_settings,
            'webex',
            exception_msg=
            "Wrong format was given to `--health-webex`. No value required. This is flag. If provide, True(webex notification enabled)."
        )

        if self.runtime.args.health_notify_webex or self.runtime.args.health_webex:
            runtime.health_webex = {}
            runtime.health_webex[
                'token'] = self.runtime.args.webex_token or cfg.get(
                    'webex.token')
            runtime.health_webex[
                'space'] = self.runtime.args.webex_space or cfg.get(
                    'webex.space')
            runtime.health_webex[
                'email'] = self.runtime.args.webex_email or cfg.get(
                    'webex.email')
            if not runtime.health_webex['token']:
                raise Exception(
                    'WebEx Token not given as argument or in config. No '
                    'WebEx notification will be sent')

            runtime.health_webex['headers'] = {
                'Authorization':
                'Bearer {}'.format(runtime.health_webex['token']),
                'Content-Type': 'application/json'
            }

            if not runtime.health_webex['space'] and not runtime.health_webex[
                    'email']:
                raise Exception(
                    'No Space ID or email specified, No WebEx Teams '
                    'notification will be sent')

            # webex notification template/url
            runtime.health_webex['msg'] = MESSAGE_TEMPLATE
            runtime.health_webex['url'] = MESSAGE_URL

        if not source:
            # Block testcase when error is found
            raise Exception(
                "Couldn't find 'pyats_health_processors' section in health.yaml."
            )

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
        if not section_names:
            # Block testcase when error is found
            raise Exception("Couldn't find any 'test_sections'.")
        processors = task.kwargs.setdefault('processors', {})

        # Try to add health section usage to telemetry data 
        if INTERNAL:
            try:
                add_health_usage_data(section_names)
            except Exception as e:
                logger.debug("Encountered an unexpected error while adding "
                             "health telemetry data: %s" % e)

        # loop by health items (sections)
        for section in section_names:
            for section_name, section_data in section.items():
                # add processors to pyATS
                processor_decorator = ProcessorDecorator()
                processor_method = processor_decorator.context(
                    func=health.health_dispatcher,
                    name='pyATS Health Check {section_name}'.format(
                        section_name=section_name))
                processor = functools.partial(
                    processor_method,
                    # enable processor report
                    report=True,
                    # params for health dispatcher
                    parameters={
                        'reconnect': reconnect,
                        'health_settings': health_settings,
                        'name': section_name,
                        'data': section_data
                    })
                processors.setdefault('context', []).append(processor)

        # save `pyats_health.yaml` to runtime.directory for archive
        with open(
                "{rundir}/pyats_health.yaml".format(
                    rundir=self.runtime.directory), 'w') as f:
            yaml.dump(health_loaded, f,
                      Dumper = OrderedSafeDumper,
                      default_flow_style = False)

    def post_task(self, task):
        # save to health_results.json
        if hasattr(runtime, 'health_results'):
            health_results = {
                'health_settings': runtime.health_results['health_settings'],
                'health_data': runtime.health_results['health_data']
            }
            with open("{rundir}/health_results.json".format(
                    rundir=runtime.directory),
                      'wt',
                      encoding='utf-8') as f:
                json.dump(health_results, f, ensure_ascii=False, indent=2)
                logger.info(
                    'saved pyATS Health Check data to {rundir}/health_results.json'
                    .format(rundir=runtime.directory))


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