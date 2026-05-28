import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_relay_pool


class TestUnconfigureDhcpRelayPool(TestCase):

    def test_unconfigure_dhcp_relay_pool(self):
        """Verify relay pool removal emits correct CLI command."""
        device = Mock()
        result = unconfigure_dhcp_relay_pool(device, pool_name='RELAY')
        self.assertIsNone(result)
        device.configure.assert_called_once_with('no ip dhcp pool RELAY')

    def test_unconfigure_dhcp_relay_pool_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_dhcp_relay_pool(device, pool_name='RELAY')


if __name__ == '__main__':
    unittest.main()
