from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.dhcp.configure import remove_dhcp_pool


class TestRemoveDhcpPool(TestCase):

    def test_remove_dhcp_pool(self):
        self.device = Mock()
        remove_dhcp_pool(self.device, pool_name='DS_POOL')
        self.device.configure.assert_called_once_with(
            "no ip dhcp pool DS_POOL"
        )

    def test_remove_dhcp_pool_positional(self):
        self.device = Mock()
        remove_dhcp_pool(self.device, 'DS_POOL')
        self.device.configure.assert_called_once_with(
            "no ip dhcp pool DS_POOL"
        )

    def test_remove_dhcp_pool_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            remove_dhcp_pool(self.device, 'DS_POOL')
