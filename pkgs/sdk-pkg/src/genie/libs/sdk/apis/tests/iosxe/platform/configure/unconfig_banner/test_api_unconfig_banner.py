import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfig_banner


class TestUnconfigBanner(unittest.TestCase):

    def test_unconfig_banner(self):
        device = Mock()
        device.configure = Mock()

        result = unconfig_banner(device, 'motd')

        self.assertIsNone(result)
        device.configure("no banner motd")