from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9800.configure import configure_management_ip


class TestConfigureManagementIpC9800(TestCase):

    def test_configure_management_ip_default_no_switchport_true(self):
        """Test that C9800 configure_management_ip defaults no_switchport to True"""
        device = Mock()
        
        configure_management_ip(
            device,
            interface='GigabitEthernet0',
            address={'ipv4': '10.1.1.1/24'}
        )

        # Verify device.configure was called with 'no switchport' command
        configure_calls = [str(call) for call in device.configure.call_args_list]
        assert any('no switchport' in str(call) for call in configure_calls), \
            f"Expected 'no switchport' in configure calls, but got: {configure_calls}"
