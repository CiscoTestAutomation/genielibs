import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    copy_running_config_to_flash_memory
)


class TestCopyRunningConfigToFlashMemory(unittest.TestCase):

    def test_copy_running_config_to_flash_memory(self):
        device = Mock()

        result = copy_running_config_to_flash_memory(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('copy running-config flash:backup_config',)
        )