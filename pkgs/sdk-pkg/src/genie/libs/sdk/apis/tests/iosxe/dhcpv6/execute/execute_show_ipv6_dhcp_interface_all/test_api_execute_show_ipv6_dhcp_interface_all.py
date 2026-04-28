from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.execute import execute_show_ipv6_dhcp_interface_all
from unittest.mock import Mock


class TestExecuteShowIpv6DhcpInterfaceAll(TestCase):

    def test_execute_show_ipv6_dhcp_interface_all(self):
        self.device = Mock()
        results_map = {
            'show ipv6 dhcp interface': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_ipv6_dhcp_interface_all(self.device)
        self.assertIn(
            'show ipv6 dhcp interface',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
