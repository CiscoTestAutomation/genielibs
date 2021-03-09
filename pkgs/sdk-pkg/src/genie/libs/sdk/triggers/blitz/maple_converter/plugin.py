

# python
import os
import yaml
import importlib
import logging
import functools

from copy import deepcopy
from shutil import copyfile

# pyats
from pyats.easypy import runtime
from pyats.log import managed_handlers
from pyats.kleenex import KleenexFileLoader
from pyats.easypy.plugins.bases import BasePlugin
from pyats.easypy.plugins.kleenex import KleenexPlugin
from pyats.aetest.processors.decorator import ProcessorDecorator

# genie
from genie import testbed
from genie.utils import Dq
from genie.harness.datafile.loader import TriggerdatafileLoader

logger = logging.getLogger(__name__)


class MapleCleanPlugin(BasePlugin):

    # plugin name
    name = 'mapleClean'
    parameters = {}

    @classmethod
    def configure_parser(cls, parser, legacy_cli=True):

        maple_grp = parser.add_argument_group('mapleClean')

        if legacy_cli:
            maple_file = ['-maple_testsuite']
        else:
            maple_file = ['--maple-testsuite']

        maple_grp.add_argument(*maple_file,
                                dest='testsuite_file',
                                default=None,
                                help='Specify maple yaml file')
        return parser

    def __init__(self, *args, **kwargs):
        self.maple = None
        super().__init__(*args, **kwargs)

    def update_tims_folder_id(self, task):
        """Updating tims folder id given the tims device provided in the testbed"""

        tims_device = self.runtime.testbed.testbed.custom.get('tims_device')

        if not tims_device or\
           not tims_device in self.runtime.testbed.devices:
            logger.error("{} does not exist in testbed".format(tims_device))
            return

        device = self.runtime.testbed.devices[tims_device]
        try:
             device.connect()
        except Exception as e:
            logger.error("Unable to connect to device '{}'\n{}".\
                format(device.name, str(e)))

        sh_version = device.parse('show version')
        img_file = sh_version.q.\
                     contains('software').get_values('system_image_file', 0)

        img_file = img_file.replace('bootflash:///','')
        task.kwargs['tims_folder'] = '{}/{}'.format(task.kwargs['tims_folder'] , img_file)

        try:
             device.disconnect()
        except Exception as e:
            logger.error("Unable to disconnect the device '{}'\n{}".\
                format(device.name, str(e)))

    def pre_job(self):
        pass

    # pre-task
    def pre_task(self, task, reporter):

        if not runtime.args.testsuite_file:
            return
        # updating the folder id that maple tests
        # are getting uploaded into
        if 'tims_rest' in self.runtime.args:
            self.update_tims_folder_id(task)

        if not self.runtime.args.clean_files:
            return

        kleenex = KleenexPlugin(self.runtime)
        kleenex.clean_files = self.runtime.args.clean_files

        logger.debug('Verifying clean files...')
        for clean_idx, clean_file in enumerate(kleenex.clean_files):

            if not os.path.isfile(clean_file):
                raise FileNotFoundError('the provided clean file %s does '
                                        'not exist' % clean_file)
            elif not os.access(clean_file, os.R_OK):
                raise PermissionError('the provided clean file %s is not '
                                      'readable' % clean_file)
            else:
                logger.info('Clean file %s exists and is readable.'
                            % clean_file)
                copy_to = 'testbed.clean%s.yaml' % (clean_idx+1)
                if len(kleenex.clean_files) == 1:
                    copy_to = 'testbed.clean.yaml'
                copyfile(clean_file, os.path.join(self.runtime.directory,
                                                  copy_to))

        kleenex.clean_config = KleenexFileLoader(
                     testbed = self.runtime.testbed,
                     invoke_clean = self.runtime.args.invoke_clean).load(
                        *(kleenex.clean_files or ()))
        extended_clean = deepcopy(kleenex.clean_config)

        # We must cast the <cleaners/cleaner/class> to a string
        # because the class is not pickle-able
        for cleaner in extended_clean['cleaners']:
            if isinstance(extended_clean['cleaners'][cleaner], dict):
                extended_clean['cleaners'][cleaner]['class'] = \
                    str(extended_clean['cleaners'][cleaner]['class'])

        extended_file = os.path.join(
            self.runtime.directory, 'testbed.clean.extended.yaml')

        try:
            # Save extended clean yaml to archive zip
            with open(extended_file, 'w') as f:
                yaml.dump(extended_clean, f)
        except Exception:
            # Best effort
            pass

        clean_config_clean_devices = kleenex.clean_config.get('clean_devices')

        if clean_config_clean_devices is not None:

            kleenex.clean_devices = [str(clean_config_clean_devices)]
        else:
            kleenex.clean_devices = None
        self.logfile = managed_handlers.tasklog.logfile
        kleenex.logical_testbed_file = None
        kleenex.do_bringup_clean_logic(task=task, reporter = reporter)

# Custom Plugin Entrypoints
maple_clean_plugin = {
    'plugins': {
        'MapleCleanPlugin:': {
            'class': MapleCleanPlugin,
            'enabled': True,
            'kwargs': {},
            'module': 'genie.libs.sdk.triggers.blitz.maple_converter',
            'order': 130,
            'name': 'MapleCleanPlugin:',
        },
    },
}