from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_vtp_trunk_interface,
)


class TestConfigureVtpTrunkInterface(TestCase):

    def test_configure_vtp_trunk_interface(self):
        device = Mock()
        result = configure_vtp_trunk_interface(device, 'te1/0/1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vtp trunk te1/0/1')
