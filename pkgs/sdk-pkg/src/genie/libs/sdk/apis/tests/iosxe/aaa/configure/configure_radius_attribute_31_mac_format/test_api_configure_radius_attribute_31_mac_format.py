import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_31_mac_format


class TestConfigureRadiusAttribute31MacFormat(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_radius_attribute_31_mac_format(self):
        configure_radius_attribute_31_mac_format(self.device)
        self.device.configure.assert_called_once_with(
            'radius-server attribute 31 mac format ietf upper-case'
        )
