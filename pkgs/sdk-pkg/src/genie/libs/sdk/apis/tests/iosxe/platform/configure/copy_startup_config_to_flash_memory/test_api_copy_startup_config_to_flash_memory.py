import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_startup_config_to_flash_memory


class TestCopyStartupConfigToFlashMemory(unittest.TestCase):

    def test_copy_startup_config_to_flash_memory(self):
        device = Mock()

        result = copy_startup_config_to_flash_memory(device, 60)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('copy startup-config flash:startup_config_backup',)
        )