
import re
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

    def save_configuration_to_file(
            self,
            device,
            default_dir,
            file_name,
            timeout=60):
        ''' Save current configuration to file on device
        '''
        file_path = '{}{}'.format(default_dir, file_name)
        try:
            # Instantiate a filetransferutils instance for IOSXE device
            self.filetransfer = FileUtils.from_device(device)
            self.filetransfer.copyconfiguration(source='running-config',
                                                destination=file_path,
                                                device=device,
                                                timeout_seconds=timeout)
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
            self.create_delete_checkpoint(device=device, name=self.ckname,
                                          abstract=abstract, action='create')
            # Check if checkpoint is successfully created
            self.check_checkpoint_status(device=device, name=self.ckname,
                                         abstract=abstract)
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

            # Instantiate a filetransferutils instance for IOSXE device
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
            for i in range(1, iteration):
                try:
                    self.rollback_checkpoint(device=device, name=self.ckname)
                    break
                except Exception as e:
                    if i == iteration - 1:
                        raise Exception('Unable to rollback config')
                    else:
                        log.info('Rollback configuration failed: sleeping {} '
                                 'seconds and retrying...'.format(interval))
                        time.sleep(interval)

            if delete_after_restore:
                # Delete the checkpoint
                self.create_delete_checkpoint(
                    device=device,
                    name=self.ckname,
                    abstract=abstract,
                    action='delete')

                # Check if checkpoint is successfully deleted
                self.check_checkpoint_status(
                    device=device,
                    name=self.ckname,
                    expect='delete',
                    abstract=abstract)
        elif method == 'local':
            # reover the deivce with whole running-config
            device.configure(self.run_config)
        elif method == 'config_replace':
            # delete the archive file
            dialog = Dialog([
                Statement(pattern=r'This will apply all necessary.*',
                          action='sendline(Y)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'less than running config.*',
                          action='sendline(Y)',
                          loop_continue=True,
                          continue_timer=False),
            ])

            for i in range(1, iteration):
                # configure replace location:<filename>
                output = device.execute('configure replace {}'.
                                        format(self.to_url), reply=dialog)
                if 'Rollback Done' in output:
                    break
                elif i == iteration - 1:
                    raise Exception('Unable to execute config replace')
                else:
                    log.info(
                        'Config replace failed: sleeping {} seconds before'
                        ' retrying.'.format(interval))
                    time.sleep(interval)

            # Compare restored configuration to details in file
            if compare:
                log.info(
                    "Comparing current running-config with config-replace file")

                # Default
                exclude = [
                    'device',
                    'maker',
                    'diff_ignore',
                    'callables',
                    '(Current configuration.*)',
                    '(.*Building configuration.*)',
                    '(.*Load for.*)',
                    '(.*Time source.*)']
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
            # modify the device via callable function
            # using Conf object
            self.modify_func(device=device, conf=self.conf,
                             values_dict=self.conf_argument,
                             recover=True, **self.specific_args)

    def create_delete_checkpoint(self, device, name, abstract, action):
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
                # get dir location
                dir_loc = abstract.parser.show_platform.Dir(
                    device=device).parse()
                dir_loc = dir_loc['dir']['dir'].replace(':/', '')
                # activate archive mode
                cfg_strs = [
                    "archive",
                    "path {dir}:{name}".format(
                        dir=dir_loc,
                        name=name),
                    "do-exec archive config"]
                ret = device.configure(cfg_strs)
            except Exception as e:
                raise SyntaxError(
                    "Issue sending {c}".format(
                        c=cfg_strs)) from e
            else:
                if 'ERROR' in ret:
                    raise SyntaxError("Issue sending {c}".format(c=cfg_strs))
        else:
            try:
                # get location
                location = re.search(
                    r'(([\w\-]+)\:+).*',
                    self.ckname).groups()[0]

                # delete the archive file
                dialog = Dialog([
                    Statement(pattern=r'Delete filename.*',
                              action='sendline()',
                              loop_continue=True,
                              continue_timer=False),
                    Statement(pattern=r'Do you want to delete.*',
                              action='sendline(y)',
                              loop_continue=True,
                              continue_timer=False),
                    Statement(pattern=r'Delete {}.*'.format(location),
                              action='sendline()',
                              loop_continue=True,
                              continue_timer=False),
                    Statement(pattern=r'\[confirm\]',
                              action='sendline()',
                              loop_continue=True,
                              continue_timer=False),
                ])

                device.execute('delete {}'.format(self.ckname), reply=dialog)

                # deactivate archive mode
                cfg_strs = ['archive', 'no path', 'exit']
                ret = device.configure(cfg_strs)
            except Exception as e:
                raise SyntaxError(
                    "Issue sending {c}".format(
                        c=cfg_strs)) from e
            else:
                if 'ERROR' in ret:
                    raise SyntaxError("Issue sending {c}".format(c=cfg_strs))

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
            dialog = Dialog([
                Statement(pattern=r'you want to proceed.*',
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False)])
            device.execute('configure replace {}'.format(name), reply=dialog)
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
            ret = abstract.parser.show_archive.ShowArchive(device=device)
            ret = ret.parse()
        except SchemaEmptyParserError as e:
            ret = ''
        except Exception as e:
            raise SyntaxError("Cannot parse command 'show archive'") from e

        if expect == 'create':
            if ret and 'most_recent_file' in ret['archive'] and \
               name in ret['archive']['most_recent_file']:
                self.ckname = ret['archive']['most_recent_file']
                log.info('{n} is successfully created'.format(n=name))
            else:
                raise KeyError(
                    '{n} is failed to create - no recent archive is found'.format(n=name))
        else:
            if (not ret) or ('most_recent_file' not in ret['checkpoint']):
                log.info('{n} is successfully deleted'.format(n=name))
            else:
                raise KeyError(
                    '{n} is failed to delete - recent archive still can be found'.format(n=name))
