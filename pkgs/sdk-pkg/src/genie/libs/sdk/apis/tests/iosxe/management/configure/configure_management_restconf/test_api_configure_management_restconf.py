from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_restconf
from unittest.mock import Mock


class TestConfigureManagementRestconf(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.management = {}

    def test_configure_management_restconf(self):
        """Test RESTCONF configuration with secure=False"""
        configure_management_restconf(self.device, secure=False)
        self.device.configure.assert_called_once()
        config_commands = self.device.configure.call_args[0][0]
        self.assertIn('ip http server', config_commands)
        self.assertIn('restconf', config_commands)
        self.assertNotIn('ip http secure-server', config_commands)

    def test_configure_management_restconf_from_testbed(self):
        """Test RESTCONF configuration reading interface from device.management"""
        self.device.management = {'interface': 'GigabitEthernet0/0'}
        configure_management_restconf(self.device, secure=True)
        self.device.configure.assert_called_once()
        config_commands = self.device.configure.call_args[0][0]
        self.assertIn('ip http secure-server', config_commands)
        self.assertIn('restconf', config_commands)
        self.assertIn('ip http client source-interface GigabitEthernet0/0', config_commands)

    def test_configure_management_restconf_override_testbed(self):
        """Test RESTCONF configuration overriding testbed interface"""
        self.device.management = {'interface': 'GigabitEthernet0/0'}
        configure_management_restconf(
            self.device, 
            source_interface='GigabitEthernet0/1',
            secure=True
        )
        self.device.configure.assert_called_once()
        config_commands = self.device.configure.call_args[0][0]
        self.assertIn('ip http client source-interface GigabitEthernet0/1', config_commands)
        self.assertNotIn('GigabitEthernet0/0', str(config_commands))
