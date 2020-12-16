'''
File utils base class for JunOS devices
'''

# Python
import sys
import pdb

# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.libs.parser.junos.show_platform import FileList


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, source, destination, timeout_seconds=300, vrf=None, *args,
                 **kwargs):
        ''' Copy a file to/from JunOS device '''

        # update source and destination with the valid address from testbed
        source = self.validate_and_update_url(source, device=kwargs.get('device'),
                                              vrf=vrf,
                                              cache_ip=kwargs.get('cache_ip', True))
        destination = self.validate_and_update_url(destination,
                                                   device=kwargs.get('device'), vrf=vrf,
                                                   cache_ip=kwargs.get('cache_ip', True))

        # Build command
        parsed_source = self.parse_url(source)
        parsed_dest = self.parse_url(destination)
        used_server = self.get_server(source, destination)
        username, passwd = self.get_auth(used_server)
        if passwd:
            auth = '%s:%s' % (username, passwd)
        else:
            auth = username

        # for junos we need to put only the username in the address, reconstruct
        # here
        if parsed_dest.netloc and '@' in destination:
            # Remove any password in destination
            destination = destination.replace(auth, username, 1)
        if parsed_source.netloc and '@' in source:
            # Remove any password in source
            source = source.replace(auth, username, 1)
        cmd = 'file copy {s} {d}'.format(s=source, d=destination)

        super().copyfile(source=source, destination=destination,
                         timeout_seconds=timeout_seconds, cmd=cmd,
                         used_server=used_server, *args, **kwargs)


    def dir(self, target, timeout_seconds=300, *args, **kwargs):
        ''' Retrieve filenames contained in a directory '''

        # Init
        file_list = []

        # Check if file exists
        output = self.device.parse('file list {}'.format(target))

        # Create list
        for directory in output['dir']:
            if 'files' in output['dir'][directory]:
                for file in output['dir'][directory]['files']:
                    if file == target:
                        file_list.append(file)

        return file_list


    def stat(self, target, timeout_seconds=300, *args, **kwargs):
        ''' Retrieve file details such as 'path' if present '''

        # Init
        file_details = {}

        # Check if file exists
        output = self.device.parse('file list {}'.format(target))

        # Create list
        for directory in output['dir']:
            if 'files' in output['dir'][directory]:
                file_details = output['dir'][directory]['files']

        return file_details


    def deletefile(self, target, timeout_seconds=300, *args, **kwargs):
        ''' Delete a file '''

        # Build command
        cmd = "file delete {}".format(target)

        # Configure
        try:
            ret = self.device.execute(cmd)
        except Exception as e:
            raise Exception("Issue sending '{}'".format(cmd)) from e
        else:
            if 'error' in ret:
                raise Exception("Issue sending '{}'".format(cmd))


    def renamefile(self, source, destination, timeout_seconds=300, *args, **kwargs):
        ''' Rename a file '''

        # Build command
        cmd = "file rename {s} {d}".format(s=source, d=destination)

        # Configure
        try:
            ret = self.device.execute(cmd)
        except Exception as e:
            raise Exception("Issue sending '{}'".format(cmd)) from e
        else:
            if 'error' in ret:
                raise Exception("Issue sending '{}'".format(cmd))


    def chmod(self, target, mode, timeout_seconds=300, *args, **kwargs):
        ''' Change file permissions '''

        raise NotImplementedError("The fileutils module {} does not implement "
                                  "chmod.".format(self.__module__))


    def validateserver(self, target, timeout_seconds=300, *args, **kwargs):
        ''' Make sure that the given server information is valid '''

        raise NotImplementedError("The fileutils module {} does not implement "
                                  "validateserver.".format(self.__module__))


    def copyconfiguration(self, source, destination, timeout_seconds=300, *args, **kwargs):
        ''' Copy configuration to/from device '''

        # Build copy command
        cmd = 'show {s} | save {d}'.format(s=source, d=destination)

        # Extract the server address to be used later for authentication
        try:
            used_server = self.get_server(source, destination)
        except:
            # We catch exception in the case where we copy configurations
            # between running and startup on the device
            used_server = None

        # Execute command
        super().copyconfiguration(source=source, destination=destination,
                                  cmd=cmd, timeout_seconds=timeout_seconds,
                                  used_server=used_server, *args, **kwargs)
