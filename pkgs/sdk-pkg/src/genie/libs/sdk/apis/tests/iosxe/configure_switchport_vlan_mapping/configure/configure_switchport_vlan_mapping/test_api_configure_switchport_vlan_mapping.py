from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.configure_switchport_vlan_mapping.configure import configure_switchport_vlan_mapping


class TestConfigureSwitchportVlanMapping(TestCase):

    def test_configure_switchport_vlan_mapping(self):
        device = Mock()
        result = configure_switchport_vlan_mapping(device, 'TenGigabitEthernet7/0/4', 2, 1501)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet7/0/4', 'switchport vlan mapping 2 1501'],)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()