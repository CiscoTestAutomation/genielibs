import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_pool


class TestConfigureDhcpPool(TestCase):

    def test_configure_dhcp_pool(self):
        device = Mock()
        result = configure_dhcp_pool(device, 'POOL_88', None, None, None, None, None, 'True', None, None, None, 'infinite')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp pool POOL_88', 'lease infinite'],)
        )

    def test_configure_dhcp_pool_with_class_name(self):
        """Verify class_name appends 'class <name>' to the pool config."""
        device = Mock()
        result = configure_dhcp_pool(
            device,
            pool_name='DS_VRF_2',
            vrf='vrf2',
            network='11.11.11.0',
            mask='255.255.255.0',
            lease=True,
            lease_days='0',
            lease_hrs='1',
            lease_mins='0',
            lease_time='0 1 0',
            class_name='DS_CLASS',
        )
        self.assertIsNone(result)
        called_config = device.configure.mock_calls[0].args[0]
        self.assertIn('class DS_CLASS', called_config)

    def test_configure_dhcp_pool_without_class_name(self):
        """Verify class_name=None (default) does not emit 'class' line - backward compat."""
        device = Mock()
        configure_dhcp_pool(device, pool_name='DS_VRF_1', vrf='vrf1',
                            network='11.11.11.0', mask='255.255.255.0')
        called_config = device.configure.mock_calls[0].args[0]
        self.assertNotIn('class', ' '.join(called_config))

    def test_configure_dhcp_pool_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_dhcp_pool(device, 'POOL_X')


if __name__ == '__main__':
    unittest.main()