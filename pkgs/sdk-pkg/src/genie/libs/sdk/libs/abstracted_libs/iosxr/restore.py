
import time
import logging
import collections
from unicon.eal.dialogs import Statement, Dialog

from pyats import aetest

# Filetransferutils
from pyats.utils.fileutils import FileUtils

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Genie
from genie.utils.diff import Diff, Config

# Logger
log = logging.getLogger(__name__)


class Restore(object):

    def save_configuration_to_file(self, device, default_dir, file_name):
        ''' Save current configuration to file on device
        '''
        file_path = '{}{}'.format(default_dir, file_name)
        try:
            # Instantiate a filetransferutils instance for IOSXE device
            self.filetransfer = FileUtils.from_device(device)
            self.filetransfer.copyconfiguration(source='running-config',
                                                destination=file_path,
                                                device=device)
        except Exception as e:
            log.error(e)
            raise Exception(
                "Issue saving config to {c}".format(
                    c=file_path)) from e

    def save_configuration(
            self,
            device,
            method,
            abstract,
            default_dir,
            copy_to_standby=False):
        if method == 'checkpoint':
            # compose checkpoint name
            self.ckname = self.__class__.__name__ + \
                time.ctime().replace(' ', '_').replace(':', '_')

            # Create checkpoint
            device.execute('show running-config | file '
                           'disk0:{name}'.format(name=self.ckname))

        elif method == 'local':
            self.run_config = device.execute('show running-config')

        elif method == 'config_replace':

            # Create unique filename
            self.filename = self.__class__.__name__ + \
                time.ctime().replace(' ', '_').replace(':', '_')

            # Set from/to locations
            self.from_url = 'running-config'
            self.to_url = '{dir}{filename}'.format(
                filename=self.filename, dir=default_dir[device.name])

            # Instantiate a filetransferutils instance for IOSXR device
            self.filetransfer = FileUtils.from_device(device)

            # Execute copy running-config to location:<filename>
            self.filetransfer.copyconfiguration(source=self.from_url,
                                                destination=self.to_url,
                                                device=device)

            if copy_to_standby:
                self.stby_url = '{dir}{filename}'.format(
                    dir='stby-{}' .format(default_dir[device.name]), filename=self.filename)

                # copy config to stby-bootflash:
                self.filetransfer.copyconfiguration(source=self.from_url,
                                                    destination=self.stby_url,
                                                    device=device)

            # Verify location:<filename> exists
            created = self.filetransfer.stat(target=self.to_url, device=device)
            if created:
                log.info("Successfully created '{}'".format(self.to_url))
            else:
                raise Exception("Unable to create '{}'".format(self.to_url))

            # Return filename generated to caller
            return self.to_url

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
            delete_after_restore=True,
            **kwargs):
        if method == 'checkpoint':
            # Enable the feature
            dialog = Dialog([
                Statement(pattern=r'\[no\]',
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False)])

            for i in range(1, iteration):
                # replace config with checkpoint
                cfg = 'load disk0:{name}\n'\
                    'commit replace'.format(name=self.ckname)
                output = device.configure(cfg, reply=dialog)
                if 'fail' not in output:
                    break
                elif i == iteration - 1:
                    raise Exception('Failed to rollback config to checkpoint')
                else:
                    log.info('Rollback checkpoint failed: sleeping {} seconds '
                             'and retrying...'.format(interval))
                    time.sleep(interval)

            if delete_after_restore:
                # need to delete the config file on the device
                dialog = Dialog([
                    Statement(pattern=r'\[confirm\]',
                              action='sendline(y)',
                              loop_continue=True,
                              continue_timer=False)])
                device.execute('delete disk0:{name}'.format(name=self.ckname),
                               reply=dialog)

        # Keeping them for later enhancement
        elif method == 'local':
            pass
        elif method == 'config_replace':
            for i in range(1, iteration):
                # Execute commit replace
                cmd = "load {}\n"\
                      "commit replace".format(self.to_url)
                output = device.configure(cmd)
                if 'Failed to commit' not in output:
                    break
                elif i == iteration - 1:
                    raise Exception('Unable to execute commit replace')
                else:
                    log.info(
                        'Commit replace failed: sleeping {} seconds before'
                        ' retrying.'.format(interval))
                    device.execute('show configuration failed')
                    time.sleep(interval)

            # Compare restored configuration to details in file
            if compare:
                log.info(
                    "Comparing current running-config with config-replace file")

                # Default
                exclude = ['device', 'maker', 'diff_ignore', 'callables',
                           '(Current configuration.*)']
                if compare_exclude:
                    if isinstance(compare_exclude, str):
                        exclude.extend([compare_exclude])
                    else:
                        exclude.extend(compare_exclude)

                # show run
                show_run_output = device.execute('show running-config')
                show_run_config = Config(show_run_output)
                show_run_config.tree()

                # location:<filename> contents
                more_file = device.execute('more {}'.format(self.to_url))
                more_file_config = Config(more_file)
                more_file_config.tree()

                # Diff 'show run' and config replace file contents
                diff = Diff(
                    show_run_config.config,
                    more_file_config.config,
                    exclude=exclude)
                diff.findDiff()

                # Check for differences
                if len(diff.diffs):
                    log.error("Differences observed betweenrunning-config and "
                              "config-replce file:'{f}' for device {d}:".
                              format(f=self.to_url, d=device.name))
                    log.error(str(diff.diffs))
                    raise Exception(
                        "Comparison between running-config and "
                        "config-replace file '{f}' failed for device"
                        " {d}".format(
                            f=self.to_url, d=device.name))
                else:
                    log.info(
                        "Comparison between running-config and config-replace"
                        "file '{f}' passed for device {d}". format(
                            f=self.to_url, d=device.name))

            if delete_after_restore:
                # Delete location:<filename>
                self.filetransfer = FileUtils.from_device(device)
                self.filename = self.to_url
                self.filetransfer.deletefile(target=self.to_url, device=device)

                # Verify location:<filename> deleted
                dir_output = self.filetransfer.dir(
                    target=self.to_url, device=device)
                for file in dir_output:
                    if self.filename in file:
                        break
                else:
                    log.info("Successfully deleted '{}'".format(self.to_url))
                    return
                raise Exception("Unable to delete '{}'".format(self.to_url))
        else:
            pass

    def create_delete_checkpoint(self, device, name, action):
        '''
            Create or Delete checkpoint

            Args:

                device (`obj`): Device Object.
                name (`str`): Checkpoint name.
                action (`str`): Create or Delete the checkpoint
                                Only accept 'create' and 'delete'
            Returns:

                None

            Raises:

                SyntaxError, AssertionError

            example:

                >>> create_delete_checkpoint(device=device,
                        name='bgp-001', action='create')
        '''

        assert action in ['create', 'delete']

        log.info('{a} checkpoint {n}'.format(a=action, n=name))
        if action == 'create':
            # create checkpoint
            try:
                ret = device.execute('checkpoint {}'.format(name))
            except Exception as e:
                raise
            else:
                if 'ERROR' in ret:
                    raise SyntaxError(ret)
        else:
            try:
                ret = device.execute('no checkpoint {}'.format(name))
            except Exception as e:
                raise
            else:
                if 'ERROR' in ret:
                    raise SyntaxError(ret)

    def rollback_checkpoint(self, device, name):
        '''
            Rollback configuration by checkpoint

            Args:

                device ('obj'): Device Object.
                name ('str'): Checkpoint name.

            Returns:

                None

            Raises:

                SyntaxError

            example:

                >>> rollback_checkpoint(device=device, name='bgp-001')
        '''
        log.info('rollback configuration by checkpoint {n}'.format(n=name))
        # rollback checkpoint
        try:
            device.execute(
                'rollback running-config checkpoint {}'.format(name))
        except Exception as e:
            raise SyntaxError('Error when running rollback running-config '
                              'checkpoint {}'.format(name)) from e

    def check_checkpoint_status(self, device, name, abstract, expect='create'):
        '''
            Check if the checkpoint is successfully created or deleted

            Args:

                device (`obj`): Device Ops.
                abstract (`obj`): Abstract Object.
                name (`str`): Checkpoint name.
                expect (`str`): Feature status.
                                Only accept 'create' and 'delete'
            Returns:

                None

            Raises:

                SyntaxError, KeyError, AssertionError

            example:

                >>> check_checkpoint_status(device=device, expect='delete',
                                            name='bgp-001',abstract=abstract)
            '''
        assert expect in ['create', 'delete']
        try:
            ret = abstract.parser.show_checkpoint.ShowCheckpointSummary(
                device=device)
            ret = ret.parse()
        except SchemaEmptyParserError as e:
            ret = ''
        except Exception as e:
            raise SyntaxError("Cannot parse command 'show checkpoint "
                              "summary'") from e

        if expect == 'create':
            if ret and name in ret['checkpoint']:
                log.info('{n} is successfully created'.format(n=name))
            else:
                raise KeyError('{n} is failed to create'.format(n=name))
        else:
            if (not ret) or (name not in ret['checkpoint']):
                log.info('{n} is successfully deleted'.format(n=name))
            else:
                raise KeyError('{n} is failed to delete'.format(n=name))
