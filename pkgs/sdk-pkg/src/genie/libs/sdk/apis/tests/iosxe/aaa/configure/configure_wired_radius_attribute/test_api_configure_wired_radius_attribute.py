import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_wired_radius_attribute


class TestConfigureWiredRadiusAttribute(unittest.TestCase):

    def test_configure_wired_radius_attribute(self):
        self.device = Mock()
        configure_wired_radius_attribute(self.device, '6', 'support-multiple')
        self.device.configure.assert_called_once_with([
            "radius-server attribute 6 support-multiple"
        ])
