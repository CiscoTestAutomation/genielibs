# python
import logging

# abstract
from genie.abstract import Lookup

# Genie Libs
from genie.libs import sdk, parser

log = logging.getLogger(__name__)


class Restore(object):

    def __init__(self, device=None):
        self.abstract = Lookup.from_device(
            device, packages={'sdk': sdk, 'parser': parser})
        self.lib = self.abstract.sdk.libs.abstracted_libs.restore.Restore()

    def save_configuration_to_file(self, device, default_dir, file_name):
        ''' Save current configuration to file on device
        '''
        try:
            self.lib.save_configuration_to_file(device, default_dir, file_name)
        except Exception as e:
            self.failed('Saving the configuration failed', from_exception=e)

    def save_configuration(self, device, method, abstract, default_dir):
        try:
            self.lib.save_configuration(
                device, method, self.abstract, default_dir)
        except Exception as e:
            self.failed('Saving the configuration failed', from_exception=e)

    def restore_configuration(self, device, method, abstract, iteration=10,
                              interval=60, delete_after_restore=True):
        try:
            self.lib.restore_configuration(
                device,
                method,
                self.abstract,
                delete_after_restore=delete_after_restore)
        except Exception as e:
            self.failed('Restoring the configuration failed', from_exception=e)

    def create_delete_checkpoint(self, device, name, action):
        self.lib.create_delete_checkpoint(device, name, action)

    def rollback_checkpoint(self, device, name):
        self.lib.rollback_checkpoint(device, name)

    def check_checkpoint_status(self, device, name, abstract, expect='create'):
        self.lib.check_checkpoint_status(device, name, self.abstract, expect)
