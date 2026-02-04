import os
import unittest
from ipaddress import IPv4Interface
from unittest.mock import Mock, patch, call
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_management


class TestConfigureManagement(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          vmtb-isr4451:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['vmtb-isr4451']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_management(self):
        result = configure_management(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_with_switchport_access(self, mock_log):
        """Test configure_management with switchport=access and vlan"""
        # Mock the API methods
        self.device.api.configure_management_vrf = Mock()
        self.device.api.configure_management_ip = Mock()
        self.device.api.configure_interface_switchport_access_vlan = Mock()
        self.device.api.configure_management_gateway = Mock()
        self.device.api.configure_management_routes = Mock()
        self.device.api.configure_management_protocols = Mock()

        # Call configure_management with switchport and vlan
        configure_management(
            self.device,
            interface='GigabitEthernet0/0',
            switchport='access',
            vlan=10,
            address={'ipv4': '192.168.1.10/24'}
        )

        # Verify configure_management_ip was called with Vlan interface
        self.device.api.configure_management_ip.assert_called_once_with(
            interface='Vlan10',
            address={'ipv4': '192.168.1.10/24'},
            vrf=None,
            dhcp_timeout=30
        )

        # Verify switchport access vlan was configured
        self.device.api.configure_interface_switchport_access_vlan.assert_called_once_with(
            interface='GigabitEthernet0/0',
            vlan=10,
            mode='access'
        )

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_with_switchport_trunk(self, mock_log):
        """Test configure_management with switchport=trunk and vlan"""
        # Mock the API methods
        self.device.api.configure_management_vrf = Mock()
        self.device.api.configure_management_ip = Mock()
        self.device.api.configure_interface_switchport_trunk = Mock()
        self.device.api.configure_management_gateway = Mock()
        self.device.api.configure_management_routes = Mock()
        self.device.api.configure_management_protocols = Mock()

        # Call configure_management with switchport and vlan
        configure_management(
            self.device,
            interface='GigabitEthernet1/0',
            switchport='trunk',
            vlan=20,
            address={'ipv4': '10.0.0.1/24'}
        )

        # Verify configure_management_ip was called with Vlan interface
        self.device.api.configure_management_ip.assert_called_once_with(
            interface='Vlan20',
            address={'ipv4': '10.0.0.1/24'},
            vrf=None,
            dhcp_timeout=30
        )

        # Verify switchport trunk was configured
        self.device.api.configure_interface_switchport_trunk.assert_called_once_with(
            interfaces=['GigabitEthernet1/0'],
            vlan_id=20,
            oper='add'
        )

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_with_switchport_no(self, mock_log):
        """Test configure_management with switchport=no"""
        # Mock the API methods
        self.device.api.configure_management_vrf = Mock()
        self.device.api.configure_management_ip = Mock()
        self.device.api.configure_management_gateway = Mock()
        self.device.api.configure_management_routes = Mock()
        self.device.api.configure_management_protocols = Mock()

        # Call configure_management with switchport=no
        configure_management(
            self.device,
            interface='GigabitEthernet2/0',
            switchport='no',
            address={'ipv4': '172.16.0.1/24'}
        )

        # Verify configure_management_ip was called with no_switchport=True
        self.device.api.configure_management_ip.assert_called_once_with(
            interface='GigabitEthernet2/0',
            address={'ipv4': '172.16.0.1/24'},
            vrf=None,
            dhcp_timeout=30,
            no_switchport=True
        )

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_switchport_access_without_vlan_raises_exception(self, mock_log):
        """Test that switchport=access without vlan raises an exception"""
        # Mock the API methods
        self.device.api.configure_management_vrf = Mock()

        # Verify exception is raised when vlan is not provided with switchport
        with self.assertRaises(Exception) as context:
            configure_management(
                self.device,
                interface='GigabitEthernet0/0',
                switchport='access',
                address={'ipv4': '192.168.1.10/24'}
            )

        self.assertIn('VLAN ID must be specified', str(context.exception))

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_switchport_trunk_without_vlan_raises_exception(self, mock_log):
        """Test that switchport=trunk without vlan raises an exception"""
        # Mock the API methods
        self.device.api.configure_management_vrf = Mock()

        # Verify exception is raised when vlan is not provided with switchport
        with self.assertRaises(Exception) as context:
            configure_management(
                self.device,
                interface='GigabitEthernet1/0',
                switchport='trunk',
                address={'ipv4': '10.0.0.1/24'}
            )

        self.assertIn('VLAN ID must be specified', str(context.exception))

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_invalid_switchport_mode_raises_exception(self, mock_log):
        """Test that invalid switchport mode raises an exception"""
        # Mock all API methods to avoid actual device calls
        self.device.api.configure_management_vrf = Mock()
        self.device.api.configure_management_ip = Mock()
        self.device.api.configure_management_gateway = Mock()
        self.device.api.configure_management_routes = Mock()
        self.device.api.configure_management_protocols = Mock()

        # Verify exception is raised for invalid switchport mode
        with self.assertRaises(Exception) as context:
            configure_management(
                self.device,
                interface='GigabitEthernet0/0',
                switchport='invalid',
                vlan=10,
                address={'ipv4': '192.168.1.10/24'}
            )

        self.assertIn('Invalid switchport mode', str(context.exception))

    @patch('genie.libs.sdk.apis.iosxe.management.configure.log')
    def test_configure_management_with_switchport_from_testbed(self, mock_log):
        """Test configure_management reads switchport and vlan from testbed"""
        # Create a testbed YAML string with management section including switchport and vlan
        testbed_with_management = f"""
        devices:
          device-with-management:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
            management:
              interface: GigabitEthernet0/0
              switchport: trunk
              vlan: 100
              address:
                ipv4: 192.168.100.10/24
        """
        testbed = loader.load(testbed_with_management)
        device = testbed.devices['device-with-management']
        device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        # Verify switchport and vlan are properly set in management
        self.assertEqual(device.management['switchport'], 'trunk')
        self.assertEqual(device.management['vlan'], 100)

        # Mock the API methods
        device.api.configure_management_vrf = Mock()
        device.api.configure_management_ip = Mock()
        device.api.configure_interface_switchport_trunk = Mock()
        device.api.configure_management_gateway = Mock()
        device.api.configure_management_routes = Mock()
        device.api.configure_management_protocols = Mock()

        # Call configure_management without explicit parameters
        # Should pick up switchport and vlan from testbed
        configure_management(device)

        # Verify configure_management_ip was called with Vlan interface from testbed
        # Note: address gets converted to IPv4Interface by the schema
        device.api.configure_management_ip.assert_called_once_with(
            interface='Vlan100',
            address={'ipv4': IPv4Interface('192.168.100.10/24')},
            vrf=None,
            dhcp_timeout=30
        )

        # Verify switchport trunk was configured with values from testbed
        device.api.configure_interface_switchport_trunk.assert_called_once_with(
            interfaces=['GigabitEthernet0/0'],
            vlan_id=100,
            oper='add'
        )
