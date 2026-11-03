from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vtp_password


class TestConfigureVtpPassword(TestCase):

    def test_configure_vtp_password(self):
        device = Mock()
        result = configure_vtp_password(device, 'cisco123')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vtp password cisco123')
