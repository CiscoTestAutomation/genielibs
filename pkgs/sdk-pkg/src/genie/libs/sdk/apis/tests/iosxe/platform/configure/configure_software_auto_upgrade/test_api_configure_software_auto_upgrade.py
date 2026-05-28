import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_software_auto_upgrade


class TestConfigureSoftwareAutoUpgrade(unittest.TestCase):

    def test_configure_software_auto_upgrade(self):
        device = Mock()

        result = configure_software_auto_upgrade(device, 'enable', '')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['software auto-upgrade enable'],)
        )