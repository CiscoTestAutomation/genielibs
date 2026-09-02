import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import delete_ip_vrf


class TestDeleteIpVrf(unittest.TestCase):

    def test_delete_ip_vrf(self):
        device = Mock()

        result = delete_ip_vrf(device, 'test')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no ip vrf test')
