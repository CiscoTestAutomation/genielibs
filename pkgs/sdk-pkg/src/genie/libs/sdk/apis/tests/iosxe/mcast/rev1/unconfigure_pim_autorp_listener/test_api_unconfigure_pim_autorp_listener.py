from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mcast.rev1.configure import unconfigure_pim_autorp_listener
from unittest.mock import Mock


class TestUnconfigurePimAutorpListener(TestCase):

    def test_unconfigure_pim_autorp_listener_global_context(self):
        """Test unconfigure_pim_autorp_listener with global context (loopback)"""
        
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with global context - loopback_number provided
        unconfigure_pim_autorp_listener(
            self.device, 
            loopback_number='0', 
            ttl='10', 
            announce=True, 
            discovery=True
        )
        
        expected_config = [
            'no ip pim autorp listener',
            'no ip pim send-rp-discovery loopback 0 scope 10',
            'no ip pim send-rp-announce loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_unconfigure_pim_autorp_listener_vrf_context(self):
        """Test unconfigure_pim_autorp_listener with VRF context"""
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with VRF and interface
        unconfigure_pim_autorp_listener(
            self.device,
            vrf='VRF1',
            intf='GigabitEthernet1/0/1',
            ttl='10',
            announce=True,
            discovery=True
        )
        
        expected_config = [
            'no ip pim vrf VRF1 autorp listener',
            'no ip pim vrf VRF1 send-rp-discovery scope 10',
            'no ip pim vrf VRF1 send-rp-announce GigabitEthernet1/0/1 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_unconfigure_pim_autorp_listener_discovery_only(self):
        """Test unconfigure_pim_autorp_listener with discovery only"""
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with discovery only, no announce
        unconfigure_pim_autorp_listener(
            self.device,
            loopback_number='0',
            ttl='10',
            announce=False,
            discovery=True
        )
        
        expected_config = [
            'no ip pim autorp listener',
            'no ip pim send-rp-discovery loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_unconfigure_pim_autorp_listener_announce_only(self):
        """Test unconfigure_pim_autorp_listener with announce only"""
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with announce only, no discovery
        unconfigure_pim_autorp_listener(
            self.device,
            loopback_number='0',
            ttl='10',
            announce=True,
            discovery=False
        )
        
        expected_config = [
            'no ip pim autorp listener',
            'no ip pim send-rp-announce loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)
