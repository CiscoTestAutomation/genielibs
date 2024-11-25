import os
import unittest
from unittest import mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.startup_config.verify import verify_ignore_startup_config

class TestStartupConfigVerify(unittest.TestCase):

    def test_verify_ignore_startup_config(self):
        device = mock.Mock()
        device.parse = mock.Mock()
        device.parse.return_value = {'version':{'next_config_register':'0x2102'}}
        output = verify_ignore_startup_config(device)
        self.assertEqual(output, True)
        device.parse.return_value = {'version':{'next_config_register':'0x2142'}}
        output = verify_ignore_startup_config(device)
        self.assertEqual(output, False)
        device.parse.return_value = {'version':{'curr_config_register':'0x2102'}}
        output = verify_ignore_startup_config(device)
        self.assertEqual(output, True)