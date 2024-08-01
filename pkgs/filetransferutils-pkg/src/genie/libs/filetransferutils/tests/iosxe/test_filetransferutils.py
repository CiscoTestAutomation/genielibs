#!/usr/bin/env python

# import python
import os
import unittest
from unittest.mock import patch
from unittest.mock import Mock, ANY

# ATS
from pyats.topology import Device, loader
from pyats.datastructures import AttrDict

# filetransferutils
from pyats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):

    testbed = """
    devices:
        csr1000v-1:
            alias: helper
            type: router
            os: iosxe
            platform: asr1k
            connections:
                ssh:
                    command: mock_device_cli --os iosxe --mock_data_dir mock_data --state execute
                    protocol: unknown
    """

    # Instantiate tesbed and device objects
    tb = loader.load(testbed)
    device = Device(testbed=tb, name='aDevice', os='iosxe')
    device1 = tb.devices["helper"]

    # Instantiate a filetransferutils instance for IOSXE device
    fu_device = FileUtils.from_device(device)
    fu_device1 = FileUtils.from_device(device1)
    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = ['flash:/nvram_config', 'flash:/.rollback_timer',
        'flash:/memleak.tcl', 'flash:/bootloader_evt_handle.log',
        'flash:/ISSUCleanGolden', 'flash:/gs_script', 'flash:/.prst_sync',
        'flash:/nvram_config_bkup', 'flash:/tech_support',
        'flash:/dc_profile_dir',
        'flash:/RestoreTue_Mar_20_12_19_11_2018-Mar-20-11-20-09.900-0',
        'flash:/vlan.dat', 'flash:/core', 'flash:/tools', 'flash:/CRDU',
        'flash:/.dbpersist',
        'flash:/RestoreTue_Mar_20_12_13_39_2018-Mar-20-11-14-38.106-0',
        'flash:/iox', 'flash:/onep', 'flash:/boothelper.log',
        'flash:/stby-vlan.dat', 'flash:/.installer']

    # Mock device output
    raw1 = '''
        copy flash:/memleak.tcl ftp://1.1.1.1//auto/tftp-ssr/memleak.tcl
        Address or name of remote host [1.1.1.1]?
        Destination filename [/auto/tftp-ssr/memleak.tcl]?
        !!
        104260 bytes copied in 0.396 secs (263283 bytes/sec)
    '''

    raw2 = '''
        Directory of flash:/

        69698  drwx             4096  Mar 20 2018 10:25:11 +00:00  .installer
        69720  -rw-          2097152  Mar 20 2018 13:09:24 +00:00  nvram_config
        69700  -rw-            90761  Mar 20 2018 10:25:27 +00:00  bootloader_evt_handle.log
        69701  drwx             4096   Feb 1 2018 13:44:32 +00:00  core
        15489  drwx             4096  Mar 20 2018 10:31:08 +00:00  .prst_sync
        30977  drwx             4096   May 2 2016 07:58:53 +00:00  .rollback_timer
        38722  drwx             4096  Mar 20 2018 10:25:43 +00:00  dc_profile_dir
        69699  -rw-               76  Mar 20 2018 10:25:46 +00:00  boothelper.log
        69705  -rw-           104260  Mar 20 2018 10:26:01 +00:00  memleak.tcl
        69706  drwx             4096   May 2 2016 08:11:23 +00:00  onep
        69714  drwx             4096  Aug 13 2016 08:55:12 +00:00  iox
        69734  -rw-             3496  Mar 11 2018 17:40:26 +00:00  vlan.dat
        69708  -rw-        617329255  Sep 27 2017 09:11:39 +00:00  ISSUCleanGolden
        69709  drwx             4096   Aug 3 2016 08:07:47 +00:00  gs_script
        69712  drwx             4096  Mar 19 2017 09:26:23 +00:00  tools
        69719  drwx             4096  Feb 12 2018 11:20:01 +00:00  .dbpersist
        69703  -rw-          2097152  Mar 20 2018 13:09:25 +00:00  nvram_config_bkup
        69729  -rw-             3496  Feb 12 2018 12:51:01 +00:00  stby-vlan.dat
        69735  -rw-            27145  Mar 20 2018 11:14:45 +00:00  RestoreTue_Mar_20_12_13_39_2018-Mar-20-11-14-38.106-0
        69721  drwx             4096  Sep 25 2017 07:59:54 +00:00  CRDU
        69727  drwx             4096  Oct 23 2017 13:40:11 +00:00  tech_support
        69736  -rw-            27145  Mar 20 2018 11:20:16 +00:00  RestoreTue_Mar_20_12_19_11_2018-Mar-20-11-20-09.900-0

        1621966848 bytes total (906104832 bytes free)
    '''

    raw3 ='''
        delete flash:memleak.tcl
        Delete filename [memleak.tcl]?
        Delete flash:/memleak.tcl? [confirm]
    '''

    raw3_1 ='''
        delete /force flash:memleak.tcl
        Delete filename [memleak.tcl]?
        Delete flash:/memleak.tcl? [confirm]
    '''

    raw4 = '''
        rename flash:memleak.tcl new_file.tcl
        Destination filename [new_file.tcl]?
    '''

    raw5 = '''
        show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock
        Writing /auto/tftp-ssr/show_clock
    '''

    raw6 = {'futlinux.check_file.return_value': '',
      'futlinux.deletefile.return_value': ''}

    raw7 = '''
         copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py
        Address or name of remote host [10.1.7.250]?
        Destination filename [/auto/tftp-ssr/test_config.py]?
        !!
        27092 bytes copied in 6.764 secs (4005 bytes/sec)
    '''
    raw8 = r'''
        copy tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki.bin flash:/meraki.bin
        Loading /auto/tftp-kmukku/9300m-tb2/meraki.bin from 172.19.1.250 (via GigabitEthernet0/0): !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        %Error opening tftp://255.255.255.255/network-confg (Timed out)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        %Error opening tftp://255.255.255.255/cisconet.cfg (Timed out)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        %Error opening tftp://255.255.255.255/switch-confg (Timed out)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        [OK - 1269880464 bytes]

        1269880464 bytes copied in 103.256 secs (12298370 bytes/sec)
    '''
    raw9 = r'''
        copy tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki1.bin flash:/meraki1.bin
        Loading /auto/tftp-kmukku/9300m-tb2/meraki1.bin from 172.19.1.250 (via GigabitEthernet0/0): !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        %Error
        [OK - 1269880464 bytes]

        1269880464 bytes copied in 103.256 secs (12298370 bytes/sec)
    '''

    raw10 = '''
        copy flash:/memleak.tcl ftp://foo@bar//auto/tftp-ssr/memleak.tcl
        Address or name of remote host [bar]?
        Destination filename [/auto/tftp-ssr/memleak.tcl]?
        !!
        104260 bytes copied in 0.396 secs (263283 bytes/sec)
    '''

    outputs = {}
    outputs['copy flash:/memleak.tcl '
            'ftp://myuser:mypw@1.1.1.1//auto/tftp-ssr/memleak.tcl']\
            = raw1
    outputs['dir'] = raw2
    outputs['delete flash:memleak.tcl'] = raw3
    outputs['delete /force flash:memleak.tcl'] = raw3_1
    outputs['rename flash:memleak.tcl new_file.tcl'] = raw4
    outputs['show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock'] = \
      raw5
    outputs['copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py'] = \
      raw7
    outputs['copy tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki.bin flash:/meraki.bin'] = \
      raw8
    outputs['copy tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki1.bin flash:/meraki1.bin'] = \
      raw9
    outputs['copy flash:/memleak.tcl ftp://foo@bar//auto/tftp-ssr/memleak.tcl'] = \
      raw10

    def mapper(self, key, timeout=None, reply= None, prompt_recovery=False, error_pattern=None):
        return self.outputs[key]

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='flash:/memleak.tcl',
            destination='ftp://1.1.1.1//auto/tftp-ssr/memleak.tcl',
            timeout_seconds='300', device=self.device)

        self.device.execute.assert_called_once_with(
            'copy flash:/memleak.tcl ftp://myuser:mypw@1.1.1.1//auto/tftp-ssr/memleak.tcl',
            prompt_recovery=True, timeout='300', reply=ANY, error_pattern=ANY)

    def test_copyfile_with_hostname(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='flash:/memleak.tcl',
            destination='ftp://foo@bar//auto/tftp-ssr/memleak.tcl',
            timeout_seconds='300', device=self.device)

        self.device.execute.assert_called_once_with(
            'copy flash:/memleak.tcl ftp://foo@bar//auto/tftp-ssr/memleak.tcl',
            prompt_recovery=True, timeout='300', reply=ANY, error_pattern=ANY)

    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(target='flash:',
            timeout_seconds=300, device=self.device)

        self.assertEqual(sorted(directory_output), sorted(self.dir_output))

    def test_stat(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        file_details = self.fu_device.stat(target='flash:memleak.tcl',
          timeout_seconds=300, device=self.device)

        self.assertEqual(file_details['last_modified_date'],
          'Mar 20 2018 10:26:01 +00:00')
        self.assertEqual(file_details['permissions'], '-rw-')
        self.assertEqual(file_details['index'], '69705')
        self.assertEqual(file_details['size'], '104260')

    def test_deletefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(target='flash:memleak.tcl',
          timeout_seconds=300, device=self.device)
        
        self.device.execute.assert_called_once_with(
            'delete flash:memleak.tcl', 
            prompt_recovery=True, timeout=300, reply=ANY, error_pattern=ANY)
        
    def test_deletefile_force(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(target='flash:memleak.tcl',
          timeout_seconds=300, force=True, device=self.device)

        self.device.execute.assert_called_once_with(
            'delete /force flash:memleak.tcl', 
            prompt_recovery=True, timeout=300, reply=ANY, error_pattern=ANY)

    def test_renamefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.renamefile(source='flash:memleak.tcl',
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

    def test_errorpattern(self):

        self.device1.connect(mit=True)
        self.fu_device1.copyfile(
            source='tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki.bin',
            destination='flash:/meraki.bin',
            timeout_seconds=300, device=self.device1)
        with self.assertRaises(Exception):
            self.fu_device1.copyfile(
                source='tftp://172.19.1.250//auto/tftp-kmukku/9300m-tb2/meraki1.bin',
                destination='flash:/meraki1.bin',
                timeout_seconds=300, device=self.device1)

    def test_abort_copy_n(self):
        self.device1.connect(mit=True)
        output = self.fu_device1.copyfile(
            source='tftp://127.0.0.1/somefile.bin',
            destination='flash:',
            timeout_seconds=300, device=self.device1)
        self.assertEqual(output.replace('\r',''), '''\
%Warning: File not a valid executable for this system
Abort Copy? [confirm]n
Loading somefile.bin from 127.0.0.1 (via GigabitEthernet0/0): !!
[OK - 5581609 bytes]''')

    def copy_to_dir_exec(self, cli, timeout=None, reply=None, prompt_recovery=False, error_pattern=None):
        self.assertEqual(cli, 'copy flash:/gs_script ftp://myuser:mypw@1.1.1.1//auto/tftp-ssr/')
        stmts = reply.extract_statements()
        for stmt in stmts:
            if stmt.pattern == r'Destination filename.*':
                self.assertEqual(stmt.args['key'], '')
        raw = r'''
            copy flash:/gs_script ftp://1.1.1.1//auto/tftp-ssr/
            Address or name of remote host [1.1.1.1]?
            Destination filename [/auto/tftp-ssr/gs_script]?
            !!
            27092 bytes copied in 6.764 secs (4005 bytes/sec)
        '''
        return raw

    def test_copyfile_to_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.copy_to_dir_exec

        # Call copyfiles
        self.fu_device.copyfile(source='flash:/gs_script',
            destination='ftp://1.1.1.1//auto/tftp-ssr/',
            timeout_seconds='300', device=self.device)

if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
