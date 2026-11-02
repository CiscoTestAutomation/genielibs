from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vtp_domain


class TestConfigureVtpDomain(TestCase):

    def test_configure_vtp_domain(self):
        device = Mock()
        result = configure_vtp_domain(device, 'cisco')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vtp domain cisco')
