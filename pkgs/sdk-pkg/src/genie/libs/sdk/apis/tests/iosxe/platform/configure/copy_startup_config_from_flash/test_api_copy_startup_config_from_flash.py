import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_startup_config_from_flash


class TestCopyStartupConfigFromFlash(unittest.TestCase):

    def test_copy_startup_config_from_flash(self):
        device = Mock()

        result = copy_startup_config_from_flash(device, 'cvvs-9410-startup.config', 60)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('copy flash:cvvs-9410-startup.config startup',)
        )