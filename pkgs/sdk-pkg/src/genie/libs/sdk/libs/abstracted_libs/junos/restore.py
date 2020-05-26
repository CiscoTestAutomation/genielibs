
# Python
import re
import time
import random
import logging

# ATS
from pyats import aetest

# Filetransferutils
from pyats.utils.fileutils import FileUtils

# Logger
log = logging.getLogger(__name__)


class Restore(object):

    def save_configuration_to_file(self, device, default_dir, file_name):
        ''' Save current configuration to file on device
        '''
        # Instantiate a filetransferutils instance for JunOS device
        file_path = '/{}/:{}'.format(default_dir, file_name)
        # Build config string
        cfg_str = "rollback 0\n save {}".format(file_path)

        # Configure
        try:
            ret = device.configure(cfg_str)
        except Exception as e:
            log.error(e)
            raise Exception(
                "Issue saving config to {c}".format(
                    c=cfg_str)) from e
        else:
            if 'error' in ret:
                raise Exception("Issue sending {c}".format(c=cfg_str))

    def save_configuration(
            self,
            device,
            method,
            abstract,
            default_dir,
            copy_to_standby=False):
        ''' Save current configuration to a checkpoint file '''

        if method == 'checkpoint' or method == 'config_replace':
            # Create unique filename
            self.to_url = self.__class__.__name__ + time.ctime().\
                replace(' ', '_').\
                replace(':', '_')

            # Save configuration
            self.create_checkpoint_file(device=device, file=self.to_url)

            # Instantiate a filetransferutils instance for JunOS device
            self.filetransfer = FileUtils.from_device(device)

            # Verify checkpoint file exists
            if self.to_url in self.filetransfer.dir(target=self.to_url,
                                                    device=device):
                log.info("Successfully created checkpoint/file '{}'".
                         format(self.to_url))
            else:
                raise Exception("Unable to create checkpoint/file '{}'".
                                format(self.to_url))

            # Return filename generated to caller
            return self.to_url

        else:
            raise NotImplementedError("save configuration using method '{}'".
                                      format(method))

    def restore_configuration(
            self,
            device,
            method,
            abstract,
            iteration=10,
            interval=60,
            compare=False,
            compare_exclude=[],
            reload_timeout=None,
            delete_after_restore=True):
        ''' Restore configuration from a checkpoint file using load replace'''

        if method == 'checkpoint' or method == 'config_replace':
            # Begin iteration
            for i in range(1, iteration):
                try:
                    self.replace_checkpoint_file(
                        device=device, file=self.to_url)
                except Exception as e:
                    log.error(e)
                    if i == iteration - 1:
                        raise Exception(
                            'Unable to load override configuration')
                    else:
                        log.info('Load override configuration failed:\n'
                                 'sleeping {} seconds and retrying...'.
                                 format(interval))
                        time.sleep(interval)
                else:
                    log.info('Load override configuration passed')
                    break

            # Instantiate a filetransferutils instance for JunOS device
            self.filetransfer = FileUtils.from_device(device)

            # Compare restored configuration to details in file
            if compare:
                log.info("Comparing current configuration with load override file")
                exclude_failed = False

                # Keys to exclude
                exclude = r'(.*Last changed.*)|(.*Last commit.*)|(.*1c1.*)|(.*\-.*)'
                if compare_exclude:
                    if isinstance(compare_exclude, str):
                        exclude += '|{}'.format(compare_exclude)
                    else:
                        for item in compare_exclude:

                            exclude += '|{}'.format(compare_exclude)

                # Copy current configuration to a file on disk
                tempfile = "tempfile{}".format(random.randint(100, 1000))
                self.filetransfer.copyconfiguration(source='configuration',
                                                    destination=tempfile,
                                                    device=device)

                # Compare the files
                diff = device.execute(
                    "file compare files {file1} {file2}". format(
                        file1=tempfile, file2=self.to_url))

                # Delete file
                self.filetransfer.deletefile(target=tempfile, device=device)

                # Check for differences
                diff = diff.strip().replace('\r', '').splitlines()
                exclude_item = []
                for item in diff:
                    if item and re.match(exclude, item):
                        continue
                    else:
                        exclude_item.append(item)
                        exclude_failed = True
                if exclude_failed:
                    # Print diffs to user
                    log.error(
                        "Differences observed between current running "
                        "configuration and load override file:'{f}' for "
                        "device {d}:".format(
                            f=self.to_url, d=device.name))
                    log.error(exclude_item)
                    if delete_after_restore:
                        # Delete files
                        self.filetransfer.deletefile(
                            target=self.to_url, device=device)
                    # Raise exception
                    raise Exception(
                        "Comparison between current running "
                        "configuration and load override file '{f}' "
                        "failed for device {d}". format(
                            f=self.to_url, d=device.name))
                else:
                    log.info(
                        "Comparison between current running configuration "
                        " and load override file '{f}' passed for device {d}". format(
                            f=self.to_url, d=device.name))

            if delete_after_restore:
                # Delete the checkpoint file
                self.filetransfer.deletefile(target=self.to_url, device=device)

                # Verify checkpoint file deleted
                if self.to_url not in self.filetransfer.dir(target=self.to_url,
                                                            device=device):
                    log.info("Successfully deleted checkpoint/file '{}'".
                             format(self.to_url))
                else:
                    raise Exception("Unable to delete checkpoint/file '{}'".
                                    format(self.to_url))
        else:
            raise NotImplementedError(
                "restore configuration using method '{}'". format(method))

    def create_checkpoint_file(self, device, file):
        ''' Creates a checkpoint file '''

        log.info('Create checkpoint file {}'.format(file))

        # Build config string
        cfg_str = "rollback 0\n save {}".format(file)

        # Configure
        try:
            ret = device.configure(cfg_str)
        except Exception as e:
            log.error(e)
            raise Exception(
                "Issue saving config to {c}".format(
                    c=cfg_str)) from e
        else:
            if 'error' in ret:
                raise Exception("Issue sending {c}".format(c=cfg_str))

    def replace_checkpoint_file(self, device, file):
        ''' Load override configuration from a checkpoint file '''

        log.info('Load override configuration with checkpoint file {}'.
                 format(file))

        # load override checkpoint file
        try:
            device.configure('load override {}'.format(file))
        except Exception as e:
            log.error(e)
            raise Exception('Error when load override configuration with '
                            'checkpoint file {}'.format(file)) from e
