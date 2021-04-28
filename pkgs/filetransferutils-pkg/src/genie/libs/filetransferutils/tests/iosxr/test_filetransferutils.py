#!/usr/bin/env python

# import python
import os
import unittest
from unittest.mock import patch
from unittest.mock import Mock

# ATS
from pyats.topology import Testbed
from pyats.topology import Device
from pyats.datastructures import AttrDict

# filetransferutils
try:
    from pyats.utils.fileutils import FileUtils
except:
    from pyats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):
    # Instantiate tesbed and device objects
    tb = Testbed(name='myTestbed')
    device = Device(testbed=tb, name='aDevice', os='iosxr')

    # Instantiate a filetransferutils instance for IOSXE device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = ['disk0:/status_file', 'disk0:/clihistory', 'disk0:/cvac',
        'disk0:/core', 'disk0:/envoke_log', 'disk0:/lost+found',
        'disk0:/pnet_cfg.log', 'disk0:/oor_aware_process',
        'disk0:/.python-history', 'disk0:/cvac.log', 'disk0:/nvgen_traces',
        'disk0:/fake_config_2.tcl', 'disk0:/ztp',
        'disk0:/config -> /misc/config', 'disk0:/memleak.tcl']


    # Mock device output
    raw1 = '''
        copy disk0:/memleak.tcl ftp://1.1.1.1//auto/tftp-ssr/memleak.tcl
        Address or name of remote host [1.1.1.1]?
        Destination filename [/auto/tftp-ssr/memleak.tcl]?
        !!
        104260 bytes copied in 0.396 secs (263283 bytes/sec)
    '''

    raw2 = '''
        dir

        Directory of /misc/scratch
           32 -rw-rw-rw- 1   824 Mar  7 06:29 cvac.log
           43 -rwxr--r-- 1     0 Mar 22 08:58 fake_config_2.tcl
           41 -rw-r--r-- 1  1985 Mar 12 14:35 status_file
           13 -rw-r--r-- 1  1438 Mar  7 14:26 envoke_log
           16 -rw-r--r-- 1    98 Mar  7 06:34 oor_aware_process
         8178 drwxr-xr-x 2  4096 Mar  7 14:27 memleak.tcl
         8177 drwx---r-x 2  4096 Mar  7 14:27 clihistory
           15 lrwxrwxrwx 1    12 Mar  7 14:26 config -> /misc/config
           12 drwxr-xr-x 2  4096 Mar  7 14:26 core
           14 -rw-r--r-- 1 10429 Mar  7 14:26 pnet_cfg.log
           11 drwx------ 2 16384 Mar  7 14:26 lost+found
         8179 drwxr-xr-x 8  4096 Mar  7 07:01 ztp
           42 -rw------- 1     0 Mar 20 11:08 .python-history
        16354 drwxr-xr-x 2  4096 Mar  7 07:22 nvgen_traces
        16353 drwxrwxrwx 3  4096 Mar  7 14:29 cvac

        1012660 kbytes total (938376 kbytes free)
    '''

    raw3 = '''
        delete disk0:fake_config_2.tcl
        Delete disk0:fake_config_2.tcl[confirm]
    '''

    raw4 = '''
        show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock
        Writing /auto/tftp-ssr/show_clock
    '''

    raw5 = {'futlinux.check_file.return_value': '',
        'futlinux.deletefile.return_value': ''}

    raw6 = '''
        copy running-config ftp://10.1.6.242//auto/tftp-ssr/fake_config_2.tcl
        Host name or IP address (control-c to abort): [10.1.6.242;default]?
        Destination username: []?rcpuser
        Destination password:
        Destination file name (control-c to abort): [/auto/tftp-ssr/fake_config_2.tcl]?
        Building configuration.
        349 lines built in 1 second
        [OK]
    '''

    raw7 =  '''
            sftp running-config myuser@1.1.1.1:/home/virl vrf management
            Thu Oct 10 15:45:18.989 UTC
            Connecting to 172.16.1.250...
            Password:

            /misc/disk1/running-config
              Overwrite /home/virl/running-config on host 172.16.1.250, continu? [
              yes/no]: yes
              Transferred 11332 Bytes
              11332 bytes copied in 0 sec (251822)bytes/sec
    '''
    outputs = {}
    outputs['copy disk0:/fake_config_2.tcl '
        'ftp://myuser:mypw@1.1.1.1//auto/tftp-ssr/fake_config_2.tcl'] = raw1
    outputs['dir'] = raw2
    outputs['delete disk0:fake_config.tcl'] = raw3
    outputs['show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock'] = \
        raw4
    outputs['copy running-config ftp://10.1.6.242//auto/tftp-ssr/fake_config_2.tcl'] = \
        raw6
    outputs['sftp running-config myuser@1.1.1.1:/home/virl'] = raw7
    def mapper(self, key, timeout=None, reply= None, prompt_recovery=False, error_pattern=None):
        return self.outputs[key]

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='disk0:/fake_config_2.tcl',
            destination='ftp://1.1.1.1//auto/tftp-ssr/fake_config_2.tcl',
            timeout_seconds='300', device=self.device)

    def test_copyfile_sftp(self):
        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='running-config',
                                destination='sftp://1.1.1.1//home/virl',
                                device=self.device)

    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(target='disk0:',
            timeout_seconds=300, device=self.device)

        self.assertEqual(sorted(directory_output), sorted(self.dir_output))

    def test_stat(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        file_details = self.fu_device.stat(target='disk0:memleak.tcl',
          timeout_seconds=300, device=self.device)

        self.assertEqual(file_details['index'],
          '8178')
        self.assertEqual(file_details['date'], 'Mar 7 14:27')
        self.assertEqual(file_details['permission'], 'drwxr-xr-x')
        self.assertEqual(file_details['size'], '4096')

    def test_deletefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(target='disk0:fake_config.tcl',
          timeout_seconds=300, device=self.device)

    def test_renamefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        with self.assertRaisesRegex(
            NotImplementedError, "The fileutils module genie.libs."
            "filetransferutils.plugins.iosxr.fileutils does not implement "
            "renamefile."):
            self.fu_device.renamefile(source='disk0:fake_config.tcl',
              destination='memleak.tcl',
                timeout_seconds=300, device=self.device)

    @patch('genie.libs.filetransferutils.plugins.fileutils.FileUtils.validateserver',
        return_value=raw5)
    def test_validateserver(self, raw5):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.validateserver(
            target='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
            timeout_seconds=300, device=self.device)

    def test_copyconfiguration(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.copyconfiguration(source='running-config',
          destination='ftp://10.1.6.242//auto/tftp-ssr/fake_config_2.tcl',
          timeout_seconds=300, device=self.device)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4