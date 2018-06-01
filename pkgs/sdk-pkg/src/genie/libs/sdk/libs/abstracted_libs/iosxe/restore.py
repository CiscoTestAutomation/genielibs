
import re
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
            self.to_url = '{dir}{filename}'.format(filename=self.filename,
                                                   dir=default_dir[device.name])

            # Instantiate a filetransferutils instance for IOSXE device
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
            self.rollback_checkpoint(device=device, name=self.ckname)

            # Delete the checkpoint
            self.create_delete_checkpoint(device=device, name=self.ckname,
                                          abstract=abstract, action='delete')

            # Check if checkpoint is successfully deleted
            self.check_checkpoint_status(device=device, name=self.ckname,
                                         expect='delete', abstract=abstract)
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
                ])

            # configure replace location:<filename>
            device.execute('configure replace {}'.format(self.to_url),
                           reply=dialog)

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
                dir_loc = abstract.parser.show_platform.Dir(device=device).parse()
                dir_loc = dir_loc['dir']['dir'].replace(':/', '')
                # activate archive mode
                cfg_str = '''
                          archive
                          path {dir}:{name}
                          do-exec archive config
                          '''
                ret = device.configure(cfg_str.format(dir=dir_loc, name=name))
            except Exception as e:
                raise SyntaxError("Issue seding {c}".format(c=cfg_str)) from e
            else:
                if 'ERROR' in ret:
                    raise SyntaxError("Issue seding {c}".format(c=cfg_str)) from e
        else:
            try:
                # get location
                location = re.search('(([\w\-]+)\:+).*', self.ckname).groups()[0]

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
                cfg_str = '''
                          archive
                          no path
                          exit
                          '''
                ret = device.configure(cfg_str)
            except Exception as e:
                raise SyntaxError("Issue seding {c}".format(c=cfg_str)) from e
            else:
                if 'ERROR' in ret:
                    raise SyntaxError("Issue seding {c}".format(c=cfg_str)) from e


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
                raise KeyError('{n} is failed to create - no recent archive is found'.format(n=name))
        else:
            if (not ret) or ('most_recent_file' not in ret['checkpoint']):
                log.info('{n} is successfully deleted'.format(n=name))
            else:
                raise KeyError('{n} is failed to delete - recent archive still can be found'.format(n=name))

