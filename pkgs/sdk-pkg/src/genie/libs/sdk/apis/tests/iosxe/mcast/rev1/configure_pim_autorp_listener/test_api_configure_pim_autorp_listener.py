from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mcast.rev1.configure import configure_pim_autorp_listener
from unittest.mock import Mock


class TestConfigurePimAutorpListener(TestCase):

    def test_configure_pim_autorp_listener_global(self):
        """Test configure_pim_autorp_listener with global context (loopback)"""
        
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with global context - loopback_number provided
        configure_pim_autorp_listener(
            self.device, 
            loopback_number='0', 
            ttl='10', 
            announce=True, 
            discovery=True
        )
        
        expected_config = [
            'ip pim autorp listener',
            'ip pim send-rp-discovery loopback 0 scope 10',
            'ip pim send-rp-announce loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_configure_pim_autorp_listener_vrf(self):
        """Test configure_pim_autorp_listener with VRF context"""
        
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with VRF context - vrf and intf provided
        configure_pim_autorp_listener(
            self.device,
            vrf='VRF1',
            intf='GigabitEthernet1/0/1',
            ttl='10',
            announce=True,
            discovery=True
        )
        
        expected_config = [
            'ip pim vrf VRF1 autorp listener',
            'ip pim vrf VRF1 send-rp-discovery scope 10',
            'ip pim vrf VRF1 send-rp-announce GigabitEthernet1/0/1 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_configure_pim_autorp_listener_discovery_only(self):
        """Test configure_pim_autorp_listener with discovery only"""
        
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with discovery only, no announce
        configure_pim_autorp_listener(
            self.device,
            loopback_number='0',
            ttl='10',
            announce=False,
            discovery=True
        )
        
        expected_config = [
            'ip pim autorp listener',
            'ip pim send-rp-discovery loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)

    def test_configure_pim_autorp_listener_announce_only(self):
        """Test configure_pim_autorp_listener with announce only"""
        
        self.device = Mock()
        self.device.api.get_running_config_section.return_value = ''
        
        # Test with announce only, no discovery
        configure_pim_autorp_listener(
            self.device,
            loopback_number='0',
            ttl='10',
            announce=True,
            discovery=False,
        )
        
        expected_config = [
            'ip pim autorp listener',
            'ip pim send-rp-announce loopback 0 scope 10'
        ]
        
        self.device.configure.assert_called_once_with(expected_config)
