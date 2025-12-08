from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_protocols
from unittest.mock import Mock, patch


class TestConfigureManagementProtocols(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'xyz'
        self.device.management = {}
        
        # Mock all the API methods that might be called
        self.device.api.configure_management_ssh = Mock()
        self.device.api.configure_management_telnet = Mock()
        self.device.api.configure_management_netconf = Mock()
        self.device.api.configure_management_gnmi = Mock()

    def test_configure_management_protocols(self):
        result = configure_management_protocols(self.device, ['ssh', 'telnet', 'netconf', 'gnmi'])
        
        # Verify each protocol configuration was called
        self.device.api.configure_management_ssh.assert_called_once()
        self.device.api.configure_management_telnet.assert_called_once()
        self.device.api.configure_management_netconf.assert_called_once()
        self.device.api.configure_management_gnmi.assert_called_once()
        
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_management_protocols_1(self):
        result = configure_management_protocols(self.device, ['ssh', 'telnet', 'netconf', {'gnmi': {'enable': True, 'server': True}}])
        
        # Verify each protocol configuration was called
        self.device.api.configure_management_ssh.assert_called_once()
        self.device.api.configure_management_telnet.assert_called_once()
        self.device.api.configure_management_netconf.assert_called_once()
        self.device.api.configure_management_gnmi.assert_called_once_with(enable=True, server=True)
        
        expected_output = None
        self.assertEqual(result, expected_output)
