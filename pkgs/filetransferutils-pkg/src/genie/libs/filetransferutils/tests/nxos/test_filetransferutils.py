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

# unicon
from unicon.core.errors import SubCommandFailure

# filetransferutils
try:
    from pyats.utils.fileutils import FileUtils
except:
    from pyats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):
    # Instantiate tesbed and device objects
    tb = Testbed(name='myTestbed')
    device = Device(testbed=tb, name='aDevice', os='nxos')

    # Instantiate a filetransferutils instance for NXOS device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = ['bootflash:/ISSUCleanGolden.system.gbin',
        'bootflash:/ISSUCleanGolden.cfg', 'bootflash:/platform-sdk.cmd',
        'bootflash:/virt_strg_pool_bf_vdc_1/', 'bootflash:/virtual-instance/',
        'bootflash:/virtual-instance.conf', 'bootflash:/.rpmstore/',
        'bootflash:/.swtam/', 'bootflash:/scripts/']

    # Mock device output
    raw1 = '''
        copy bootflash:/virtual-instance.conf ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf
        Enter username: rcpuser
        Password:
        ***** Transfer of file Completed Successfully *****
        Copy complete.
    '''

    raw2 = '''
        dir
               4096    Jan 25 21:00:53 2017  .rpmstore/
               4096    Jan 25 21:01:08 2017  .swtam/
                390    Jan 25 21:36:20 2017  ISSUCleanGolden.cfg
          752699904    Jan 25 21:36:26 2017  ISSUCleanGolden.system.gbin
                  0    Jan 25 21:35:55 2017  platform-sdk.cmd
               4096    Jan 25 21:01:57 2017  scripts/
               4096    Jan 25 21:02:02 2017  virt_strg_pool_bf_vdc_1/
               4096    Jan 25 21:01:21 2017  virtual-instance/
                 59    Jan 25 21:01:11 2017  virtual-instance.conf

        Usage for bootflash://
         1150812160 bytes used
         2386407424 bytes free
         3537219584 bytes total
    '''

    raw3 = '''
        delete bootflash:new_file.tcl
        Do you want to delete "/new_file.tcl" ? (yes/no/abort)   [y]
    '''

    raw4 =  '''
        move bootflash:mem_leak.tcl new_file.tcl
    '''

    raw5 = '''
        show clock > ftp://10.1.7.250//auto/tftp-ssr/show_clock vrf management
        Enter username: rcpuser
        Password:
        ***** Transfer of file Completed Successfully *****
    '''

    raw6 = {'futlinux.check_file.return_value': '',
        'futlinux.deletefile.return_value': ''}

    raw7 ='''
        copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py vrf management
        Trying to connect to tftp server......
        Connection to Server Established.
        [                         ]         0.50KB[#                        ]         4.50KB[##                       ]         8.50KB[###                      ]        12.50KB                                                                                    TFTP put operation was successful
        Copy complete, now saving to disk (please wait)...
        Copy complete.
    '''
    raw8 = '''
        copy running-config sftp://1.1.1.1//home/virl vrf management
        Enter username: myuser

        The authenticity of host '1.1.1.1 (1.1.1.1)' can't be established.
        ECDSA key fingerprint is SHA256:Q37/fav3nPJT5Y+7IsgST4uN0c2tyToJiDF/gp+wItA.
        Are you sure you want to continue connecting (yes/no)? yes
        Warning: Permanently added '1.1.1.1' (ECDSA) to the list of known hosts.
        Outbound-ReKey for 1.1.1.1:22
        Inbound-ReKey for 1.1.1.1:22
        myuser@1.1.1.1's password:
        Connected to 1.1.1.1.
        sftp> put  /var/tmp/vsh/R3_nx-running-config  /home/virl
        Uploading /var/tmp/vsh/R3_nx-running-config to /home/virl/R3_nx-running-config
        /var/tmp/vsh/R3_nx-running-config
                                                                                                                                                                                                                                                                                                                                    /var/tmp/vsh/R3_nx-running-config                                                                                                                                                                                                                                                                                                                                                                                                                                                            100%   14KB 355.1KB/s   00:00
    '''
    raw9 = '''
        copy bootflash:/virtual-instance.conf ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf
        Enter username: rcpuser
        ftp: connect: No route to host
        ***** Transfer of file aborted, server not connected *****
        Error during copy
        ***** Transfer of file aborted *****

    '''

    raw11 = """
    copy tftp://192.168.0.253//auto/tftp-ssr/golden/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin bootflash:/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin vrf management
    no such file or directory (invalid server)
    """

    outputs = {}
    outputs['copy bootflash:/virtual-instance.conf '
        'ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf vrf management'] = raw1
    outputs['dir'] = raw2
    outputs['delete bootflash:new_file.tcl'] = raw3
    outputs['move bootflash:mem_leak.tcl new_file.tcl'] = raw4
    outputs['show clock > ftp://1.1.1.1//auto/tftp-ssr/show_clock vrf management'] = raw5
    outputs['copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py vrf management'] = raw7
    outputs['copy running-config sftp://myuser@1.1.1.1//home/virl vrf management'] = raw8
    outputs['copy running-config sftp://myuser@1.1.1.1//home/virl'] = raw8
    outputs['copy bootflash:/virtual-instance.conf '
        'ftp://10.1.0.214//auto/tftp-ssr/virtual-instance.conf vrf management'] = raw9
    outputs['copy tftp://192.168.0.253//auto/tftp-ssr/golden/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin ' \
            'bootflash:/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin vrf management'] = raw11

    def mapper(self, key, timeout=None, reply=None, prompt_recovery=False, error_pattern=None):
        output = self.outputs[key]
        if error_pattern:
            for line in output.splitlines():
                for word in error_pattern:
                    if word in line:
                        raise SubCommandFailure('Error message caught in the following line: "{line}"'.format(line=line))
        return output

    def is_valid_ip_mapper(self, ip, device=None, vrf=None, cache_ip=None):
        return ip!='2.2.2.2'

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='bootflash:/virtual-instance.conf',
            destination='ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf',
            timeout_seconds='300', device=self.device)

    def test_copyfile_exception(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        with self.assertRaises(SubCommandFailure):
            self.fu_device.copyfile(source='bootflash:/virtual-instance.conf',
                destination='ftp://10.1.0.214//auto/tftp-ssr/virtual-instance.conf',
                timeout_seconds='300', device=self.device)

    def test_copyfile_sftp(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles with vrf None (for default)
        self.fu_device.copyfile(source='running-config',
            destination='sftp://1.1.1.1//home/virl',
            vrf=None, device=self.device)

        self.assertEqual(self.device.execute.mock_calls[0][1][0],
                         'copy running-config sftp://myuser@1.1.1.1//home/virl '
                         'vrf management')

    def test_copyfile_sftp_no_vrf(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles with vrf empty string
        self.fu_device.copyfile(source='running-config',
            destination='sftp://1.1.1.1//home/virl',
            vrf='', device=self.device)

        self.assertEqual(self.device.execute.mock_calls[0][1][0],
                         'copy running-config sftp://myuser@1.1.1.1//home/virl')

    def test_validate_and_update_url(self):
        self.fu_device.is_valid_ip = Mock()
        self.fu_device.is_valid_ip.side_effect = self.is_valid_ip_mapper
        # set multiple ip for the server
        self.device.testbed.servers.server_name['address']=['2.2.2.2', '1.1.1.1']
        not_reachable_url = self.fu_device.validate_and_update_url('sftp://2.2.2.2//home/virl',
                                                                    device=self.device)
        reachable_url = self.fu_device.validate_and_update_url('sftp://1.1.1.1//home/virl',
                                                                device=self.device)
        servername_url = self.fu_device.validate_and_update_url('sftp://server_name//home/virl',
                                                                device=self.device)
        self.assertEqual(not_reachable_url, 'sftp://myuser@1.1.1.1//home/virl')
        self.assertEqual(reachable_url, 'sftp://myuser@1.1.1.1//home/virl')
        self.assertEqual(servername_url, 'sftp://myuser@1.1.1.1//home/virl')
        self.device.testbed.servers.server_name['address'] = '1.1.1.1'


    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(target='bootflash:',
            timeout_seconds=300, device=self.device)

        self.assertEqual(sorted(directory_output), sorted(self.dir_output))

    def test_stat(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        file_details = self.fu_device.stat(
            target='bootflash:virtual-instance.conf',
            timeout_seconds=300, device=self.device)

        self.assertEqual(file_details['time'], '21:01:11')
        self.assertEqual(file_details['date'], 'Jan 25 2017')
        self.assertEqual(file_details['size'], '59')

    def test_deletefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(target='bootflash:new_file.tcl',
          timeout_seconds=300, device=self.device)

    def test_renamefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.renamefile(source='bootflash:mem_leak.tcl',
          destination='new_file.tcl',
          timeout_seconds=300, device=self.device)

    @patch('genie.libs.filetransferutils.plugins.fileutils.FileUtils.validateserver',
        return_value=raw6)
    def test_validateserver(self, raw6):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.validateserver(
            target='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
            timeout_seconds=300, device=self.device)

    def test_copyconfiguration(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.copyconfiguration(source='running-config',
          destination='tftp://10.1.7.250//auto/tftp-ssr/test_config.py',
          timeout_seconds=300, device=self.device)

    def test_ftp_invalidserver(self):
        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        with self.assertRaises(SubCommandFailure):
            self.fu_device.copyfile(source='tftp://192.168.0.253//auto/tftp-ssr/golden/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin',
                                    destination='bootflash:/fake_extrafake2_n7000-s2-kickstart.8.4.4.bin',
                                    vrf='management')

if __name__ == '__main__':
    unittest.main()
