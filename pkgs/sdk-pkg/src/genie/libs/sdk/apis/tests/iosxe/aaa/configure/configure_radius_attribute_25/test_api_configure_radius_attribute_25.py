import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_25


class TestConfigureRadiusAttribute25(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_radius_attribute_25(self):
        configure_radius_attribute_25(self.device)
        self.device.configure.assert_called_once_with(
            'radius-server attribute 25 access-request include'
        )
