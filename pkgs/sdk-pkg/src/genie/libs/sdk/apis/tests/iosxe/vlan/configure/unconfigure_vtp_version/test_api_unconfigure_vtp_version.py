import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vtp_version


class TestUnconfigureVtpVersion(unittest.TestCase):

    def test_unconfigure_vtp_version(self):
        device = Mock()

        result = unconfigure_vtp_version(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no vtp version')
