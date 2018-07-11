
import time
import logging
import collections
from unicon.eal.dialogs import Statement, Dialog

from ats import aetest

# Filetransferutils
from ats.utils.fileutils import FileUtils

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


class Restore(object):

    def save_configuration(self, device, method, abstract, default_dir):
        if method == 'checkpoint':
            # compose checkpoint name
            self.ckname = self.__class__.__name__ + \
                          time.ctime().replace(' ', '_').replace(':', '_')

            # Create checkpoint
            device.execute('show running-config | file '\
                           'disk0:{name}'.format(name=self.ckname))

        elif method == 'local':
            self.run_config = device.execute('show running-config')

        elif method == 'config_replace':

            # Create unique filename
            self.filename = self.__class__.__name__ + \
                                time.ctime().replace(' ', '_').replace(':', '_')

            # Set from/to locations
            self.from_url = 'running-config'
            self.to_url = '{dir}{filename}'.format(filename=self.filename,
                                                   dir=default_dir[device.name])

            # Instantiate a filetransferutils instance for IOSXR device
            self.filetransfer = FileUtils.from_device(device)

            # Execute copy running-config to location:<filename>
            self.filetransfer.copyconfiguration(source=self.from_url,
                                                destination=self.to_url,
                                                device=device)

            # Verify location:<filename> exists
            created = self.filetransfer.stat(target=self.to_url, device=device)
            if created:
                log.info("Successfully created '{}'".format(self.to_url))
            else:
                raise Exception("Unable to create '{}'".format(self.to_url))

    def restore_configuration(self, device, method, abstract):
        if method == 'checkpoint':
            # Enable the feature
            dialog = Dialog([
                Statement(pattern=r'\[no\]',
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False)])
            cfg ='load disk0:{name}\n'\
                 'commit replace'.format(name=self.ckname)
            device.configure(cfg, reply=dialog)

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
            # Build command
            cmd = "load {}\n"\
                  "commit replace".format(self.to_url)

            # Execute the following commands:
            #    PE1# load location:<filename>
            #    PE1# commit replace
            device.configure(cmd)

            # Delete location:<filename>
            self.filetransfer.deletefile(target=self.to_url, device=device)

            # Verify location:<filename> deleted
            dir_output = self.filetransfer.dir(target=self.to_url,device=device)
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
            device.execute('rollback running-config checkpoint {}'.format(name))
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

