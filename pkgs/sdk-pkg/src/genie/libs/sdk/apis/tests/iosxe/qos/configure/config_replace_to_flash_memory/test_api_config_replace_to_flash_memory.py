import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    config_replace_to_flash_memory
)


class TestConfigReplaceToFlashMemory(unittest.TestCase):

    def test_config_replace_to_flash_memory(self):
        device = Mock()

        result = config_replace_to_flash_memory(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('configure replace flash:backup_config',)
        )