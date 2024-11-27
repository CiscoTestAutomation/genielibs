import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_8


class TestConfigureRadiusAttribute8(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_radius_attribute_8(self):
        configure_radius_attribute_8(self.device)
        self.device.configure.assert_called_once_with(
            'radius-server attribute 8 include-in-access-req'
        )
