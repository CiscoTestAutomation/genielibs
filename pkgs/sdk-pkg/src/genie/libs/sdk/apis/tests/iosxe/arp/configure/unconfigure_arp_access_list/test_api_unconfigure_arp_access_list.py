import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_arp_access_list


class TestUnconfigureArpAccessList(unittest.TestCase):

    def test_unconfigure_arp_access_list(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_arp_access_list(device, 'access-list', 'allowed-acl')
        self.assertIsNone(result)
        device.configure.assert_called_once_with(['no arp access-list allowed-acl'])