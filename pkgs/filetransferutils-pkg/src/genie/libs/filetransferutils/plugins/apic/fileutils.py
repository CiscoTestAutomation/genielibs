from .. import FileUtils as FileUtilsDeviceBase

class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, source, destination, timeout_seconds=300, vrf=None, *args,
                 **kwargs):
        ''' Copy a file to/from APIC device '''

        used_server = self.get_server(source, destination)
        username, _ = self.get_auth(used_server)
        ssh_protocol = {'scp', 'sftp'}
        quiet = kwargs.get('quiet', False)

        # if protocol is scp or sftp
        # sftp only support download
        for protocol in ssh_protocol:
            if '{}:'.format(protocol) in source or '{}:'.format(protocol) in destination:
                # scp/sftp requires username in the address
                if '{}:'.format(protocol) in source:
                    source = '{username}@{url}'.format(username=username, url=source)
                elif '{}:'.format(protocol) in destination:
                    destination = '{username}@{url}'.format(username=username, url=destination)

                # still use scp if user provided sftp because sftp is interactive
                # will change this if one day we can support sftp on linux
                # if quiet is true it will hide the copy progress
                cmd = 'scp {q}{s} {d}'.format(q='-q ' if quiet else '',
                                              protocol=protocol,
                                              s=source.replace('{}://'.format(protocol),
                                                               '').replace('//', ':/'),
                                              d=destination.replace(
                                                  '{}://'.format(protocol),
                                                  '').replace('//', ':/'))
                break

        else:
            raise NotImplementedError('Only SFTP and SCP protocols are currently supported for APIC')

        super().copyfile(source=source, destination=destination,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            *args, **kwargs)

    def deletefile(self, target, timeout_seconds=300, *args, **kwargs):
        """ Delete a file

            Parameters
            ----------
                target : `str`
                    The URL of the file whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.
                    Default: 300 seconds

            Returns
            -------
                None

            Raises
            ------
            Exception
                When a device object is not present or device execution encountered
                an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # delete a specific file on device directory 'flash:'
                >>> directory_output = fu_device.deletefile(
                ...     target='flash:memleak_bckp.tcl',
                ...     timeout_seconds=300, device=device)

        """

        # rm -f /data/techsupport/local.tgz
        cmd = 'rm -f {f}'.format(f=target)

        self.send_cli_to_device(cli=cmd, timeout_seconds=timeout_seconds, **kwargs)
