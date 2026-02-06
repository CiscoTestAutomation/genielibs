import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_pnp_startup_vlan


class TestConfigurePnpStartupVlan(TestCase):

    def test_configure_pnp_startup_vlan(self):
        device = Mock()
        result = configure_pnp_startup_vlan(device, '1200', 'GigabitEthernet1/0/10')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/10', 'pnp startup-vlan 1200'],)
        )


if __name__ == '__main__':
    unittest.main()