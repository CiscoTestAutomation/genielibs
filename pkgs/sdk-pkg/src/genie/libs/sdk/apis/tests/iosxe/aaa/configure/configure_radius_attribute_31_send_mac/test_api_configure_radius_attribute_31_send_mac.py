import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_attribute_31_send_mac


class TestConfigureRadiusAttribute31SendMac(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_radius_attribute_31_send_mac(self):
        configure_radius_attribute_31_send_mac(self.device)
        self.device.configure.assert_called_once_with(
            'radius-server attribute 31 send nas-port-detail mac-only'
        )
