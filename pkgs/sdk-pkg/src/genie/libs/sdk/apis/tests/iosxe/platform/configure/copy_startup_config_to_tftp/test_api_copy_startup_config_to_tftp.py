import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_startup_config_to_tftp


class TestCopyStartupConfigToTftp(unittest.TestCase):

    def test_copy_startup_config_to_tftp(self):
        device = Mock()

        result = copy_startup_config_to_tftp(
            device,
            '202.153.144.25',
            '/auto/tftp-sjc-users4/nikhijai/startup_config_new',
            30
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('copy startup-config tftp://202.153.144.25//auto/tftp-sjc-users4/nikhijai/startup_config_new',)
        )