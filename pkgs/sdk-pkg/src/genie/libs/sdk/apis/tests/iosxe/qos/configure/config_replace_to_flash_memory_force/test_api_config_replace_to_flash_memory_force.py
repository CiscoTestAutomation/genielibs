import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    config_replace_to_flash_memory_force
)


class TestConfigReplaceToFlashMemoryForce(unittest.TestCase):

    def test_config_replace_to_flash_memory_force(self):
        device = Mock()

        result = config_replace_to_flash_memory_force(
            device,
            'stby-bootflash',
            60
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
             ('configure replace stby-bootflash:backup_config force',)
        )