import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vtp_password


class TestUnconfigureVtpPassword(unittest.TestCase):

    def test_unconfigure_vtp_password(self):
        device = Mock()

        result = unconfigure_vtp_password(device, 'cisco123')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no vtp password cisco123'
        )
