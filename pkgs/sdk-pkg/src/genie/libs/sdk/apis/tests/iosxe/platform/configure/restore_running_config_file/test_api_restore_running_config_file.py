import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import restore_running_config_file


class TestRestoreRunningConfigFile(unittest.TestCase):

    def test_restore_running_config_file(self):
        device = Mock()

        device.execute.return_value = 'no'

        result = restore_running_config_file(device, 'flash:', 'configtest', 120)

        self.assertEqual(result, 'no')