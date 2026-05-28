import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_relay_pool


class TestConfigureDhcpRelayPool(TestCase):

    def test_configure_dhcp_relay_pool(self):
        """Verify relay pool emits correct CLI commands."""
        device = Mock()
        result = configure_dhcp_relay_pool(
            device,
            pool_name='RELAY',
            relay_source_network='11.11.11.0',
            relay_source_mask='255.255.255.0',
            relay_destination='192.168.1.1',
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'ip dhcp pool RELAY',
                    ' relay source 11.11.11.0 255.255.255.0',
                    ' relay destination 192.168.1.1',
                ],
            ),
        )

    def test_configure_dhcp_relay_pool_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_dhcp_relay_pool(
                device,
                pool_name='RELAY',
                relay_source_network='10.0.0.0',
                relay_source_mask='255.255.255.0',
                relay_destination='10.0.1.1',
            )


if __name__ == '__main__':
    unittest.main()
