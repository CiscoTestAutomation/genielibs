import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vtp_mode


class TestUnconfigureVtpMode(unittest.TestCase):

    def test_unconfigure_vtp_mode(self):
        device = Mock()

        result = unconfigure_vtp_mode(device, 'transparent')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no vtp mode transparent'
        )
