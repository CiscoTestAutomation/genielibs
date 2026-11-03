from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vtp_version


class TestConfigureVtpVersion(TestCase):

    def test_configure_vtp_version(self):
        device = Mock()
        result = configure_vtp_version(device, 3)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vtp version 3')
