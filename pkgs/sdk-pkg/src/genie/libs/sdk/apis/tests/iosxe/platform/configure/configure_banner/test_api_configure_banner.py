import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_banner


class TestConfigureBanner(unittest.TestCase):

    def test_configure_banner(self):
        device = Mock()
        device.configure = Mock()

        result = configure_banner(device, 'motd')

        self.assertIsNone(result)
        device.configure(f"banner motd")