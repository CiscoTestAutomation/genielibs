#!/usr/bin/env python

import os
import unittest

from pyats.datastructures import AttrDict
from pyats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):

    def test_fu_from_device_protocol(self):
        # Instantiate a filetransferutils instance for each os and protocol
        for os_ in ['ios', 'iosxe', 'iosxr', 'nxos']:
            device = AttrDict(os=os_)
            for proto in ['ftp', 'tftp', 'scp', 'sftp', 'http']:
                fu = FileUtils.from_device(device, protocol=proto)
                self.assertIn(
                    'genie.libs.filetransferutils.plugins.{os_}.{proto}.fileutils.FileUtils'
                    .format(os_=os_, proto=proto),
                    str(fu.__class__))
                self.assertEqual(fu.protocol, proto)
                self.assertEqual(fu.os, os_)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
