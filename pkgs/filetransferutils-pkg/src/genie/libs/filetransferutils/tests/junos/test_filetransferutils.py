#!/usr/bin/env python

# import python
import unittest
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
    device = Device(testbed=tb, name='aDevice', os='junos')

    # Instantiate a filetransferutils instance for Junos device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    # Mock device output
    raw1 = '''
            file copy golden_config ftp://myuser@1.1.1.1:/test/ 
            Password for myuser@1.1.1.1:
            ftp://myuser@1.1.1.1:/test/golden_config     100% of 3040  B   11 MBps

    '''

    outputs = {}
    outputs['file copy golden_config ftp://myuser@1.1.1.1:/test/']\
         = raw1

    def mapper(self, key, timeout=None, reply= None, prompt_recovery=False, error_pattern=None):
        return self.outputs[key]

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='golden_config',
            destination='ftp://1.1.1.1:/test/',
            timeout_seconds='300', device=self.device)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4