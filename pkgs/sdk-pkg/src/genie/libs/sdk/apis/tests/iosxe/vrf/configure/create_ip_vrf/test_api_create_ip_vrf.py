import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import create_ip_vrf


class TestCreateIpVrf(unittest.TestCase):

    def test_create_ip_vrf(self):
        device = Mock()

        result = create_ip_vrf(device, 'test')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('ip vrf test')
