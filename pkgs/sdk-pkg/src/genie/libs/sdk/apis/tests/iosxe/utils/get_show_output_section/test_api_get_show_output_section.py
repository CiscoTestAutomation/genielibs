import unittest
from unittest.mock import Mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import get_show_output_section
from unicon.core.errors import SubCommandFailure


class TestGetShowOutputSection(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          c2_core_sf:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['c2_core_sf']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_show_output_section(self):
        result = get_show_output_section(self.device, 'show run', 'ospf')
        expected_output = (True,
 'key chain ospf-1\r\n'
 ' key 1\r\n'
 '  key-string ospf\r\n'
 '   cryptographic-algorithm hmac-sha-512\r\n'
 ' ip ospf 100 area 0\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ip ospf bfd\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ipv6 ospf bfd\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ip ospf bfd\r\n'
 ' ip ospf 100 area 0\r\n'
 ' ipv6 ospf 100 area 0\r\n'
 ' ipv6 ospf bfd\r\n'
 ' ospfv3 41 ipv6 area 41\r\n'
 'router ospfv3 100\r\n'
 ' nsr\r\n'
 ' graceful-restart\r\n'
 ' !\r\n'
 ' address-family ipv6 unicast\r\n'
 ' exit-address-family\r\n'
 'router ospfv3 41\r\n'
 ' !\r\n'
 ' address-family ipv6 unicast\r\n'
 '  nsr\r\n'
 ' exit-address-family\r\n'
 'router ospf 100\r\n'
 ' router-id 1.1.1.20\r\n'
 ' priority 126\r\n'
 ' nsr\r\n'
 ' nsf\r\n'
 ' redistribute connected\r\n'
 ' network 80.80.80.20 0.0.0.0 area 0\r\n'
 ' network 192.168.21.0 0.0.0.255 area 0\r\n'
 ' network 192.168.22.0 0.0.0.255 area 0\r\n'
 ' network 192.168.23.0 0.0.0.255 area 0\r\n'
 ' network 192.168.24.0 0.0.0.255 area 0\r\n'
 ' network 192.168.32.0 0.0.0.255 area 0\r\n'
 'snmp-server enable traps ospf state-change\r\n'
 'snmp-server enable traps ospf errors\r\n'
 'snmp-server enable traps ospf retransmit\r\n'
 'snmp-server enable traps ospf lsa\r\n'
 'snmp-server enable traps ospf cisco-specific state-change '
 'nssa-trans-change\r\n'
 'snmp-server enable traps ospf cisco-specific state-change shamlink '
 'interface\r\n'
 'snmp-server enable traps ospf cisco-specific state-change shamlink '
 'neighbor\r\n'
 'snmp-server enable traps ospf cisco-specific errors\r\n'
 'snmp-server enable traps ospf cisco-specific retransmit\r\n'
 'snmp-server enable traps ospf cisco-specific lsa\r\n'
 'snmp-server enable traps ospfv3 state-change\r\n'
 'snmp-server enable traps ospfv3 errors')
        self.assertEqual(result, expected_output)

    def test_get_show_output_section_with_target(self):
        device = Mock()
        device.execute.return_value = 'ip subscriber initiator unclassified mac-address'
        result = get_show_output_section(
            device, 'show running-config',
            'initiator unclassified mac-address',
            target='standby'
        )
        device.execute.assert_called_once_with(
            'show running-config | section initiator unclassified mac-address',
            target='standby'
        )
        self.assertEqual(result, (True, 'ip subscriber initiator unclassified mac-address'))

    def test_get_show_output_section_without_target(self):
        device = Mock()
        device.execute.return_value = 'some output'
        result = get_show_output_section(device, 'show run', 'ospf')
        device.execute.assert_called_once_with(
            'show run | section ospf'
        )
        self.assertEqual(result, (True, 'some output'))

    def test_get_show_output_section_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            get_show_output_section(device, 'show run', 'ospf')
