from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_show_policy_firewall_config_platform
from unittest.mock import Mock


class TestExecuteShowPolicyFirewallConfigPlatform(TestCase):

    def test_execute_show_policy_firewall_config_platform(self):
        self.device = Mock()
        results_map = {
            'show policy-firewall config platform': '''--show platform software firewall FP active bindings--
--show platform software firewall RP active bindings--
--show platform software firewall FP active pairs--
--show platform software firewall RP active pairs--
--show platform software firewall FP active parameter-maps--
Forwarding Manager Inspect Parameter-Maps
  Inspect Parameter Map: global, Index 1
  Parameter Map Type: Parameter-Map
      Global Parameter-Map
      Alerts: On, Audits: Off, Drop-Log: Off, Log flow: Off
      HSL Mode: Disabled, Host: 0.0.0.0:0, Port: 0, Template: 300 sec
      Session Rate High: 2147483647, Session Rate Low: 2147483647, Time Duration: 60 sec
      Half-Open:
        High: 2147483647, Low: 2147483647, Host: 4294967295, Host Block Time: 0
      Inactivity Times [sec]:
        DNS: 5, ICMP: 10, TCP: 3600, UDP: 30
      Inactivity Age-out Times [sec]:
        ICMP: 10, TCP: 3600, UDP: 30
      TCP Timeouts [sec]:
        SYN wait time: 30, FIN wait time: 1
      TCP Ageout Timeouts [sec]:
        SYN wait time: 30, FIN wait time: 1
      TCP RST pkt control:
        half-open: On, half-close: On, idle: On
      UDP Timeout [msec]:
        UDP Half-open time: 30000
      UDP Ageout Timeout [msec]:
        UDP Half-open time: 30000
       
      Max Sessions: Unlimited
      Number of Simultaneous Packet per Sessions: 0
      Syn Cookie and Resource Management:
        Global Syn Flood Limit: 4294967295
        Global Total Session : 4294967295
        Global Number of Simultaneous Packet per Session : 
      Global Total Session Aggressive Aging Disabled
      Global alert : Off
      Global max incomplete : 4294967295
      Global max incomplete TCP: 4294967295
      Global max incomplete UDP: 4294967295
      Global max incomplete ICMP: 4294967295
      Global max incomplete Aggressive Aging Disabled
      Per Box Configuration
        syn flood limit : 4294967295
        Total Session Aggressive Aging Disabled
        max incomplete : 4294967295
        max incomplete TCP: 4294967295
        max incomplete UDP: 4294967295
        max incomplete ICMP: 4294967295
        max incomplete Aggressive Aging Disabled
  Inspect Parameter Map: vrf-default, Index 2
  Parameter Map Type: VRF-Parameter-Map
  VRF PMAP syn flood limit : 4294967295
  VRF PMAP total session : 4294967295
  VRF PMAP total session Aggressive Aging Disabled
  VRF PMAP alert : Off
  VRF PMAP max incomplete : 4294967295
  VRF PMAP max incomplete TCP: 4294967295
  VRF PMAP max incomplete UDP: 4294967295
  VRF PMAP max incomplete ICMP: 4294967295
  VRF PMAP max incomplete Aggressive Aging Disabled
--show platform software firewall RP active parameter-maps--
Forwarding Manager Inspect Parameter-Maps
  Inspect Parameter Map: global
  Parameter Map Type: Parameter-Map
      Global Parameter-Map
      Alerts: On, Audits: Off, Drop-Log: Off, Log flow: Off
      HSL Mode: Disabled, Host: :0, Port: 0, Template: 300 sec
      Session Rate High: 2147483647, Session Rate Low: 2147483647, Time Duration: 60 sec
      Half-Open:
        High: 2147483647, Low: 2147483647, Host: 4294967295, Host Block Time: 0
      Inactivity Times [sec]:
        DNS: 5, ICMP: 10, TCP: 3600, UDP: 30
      Inactivity Age-out Times [sec]:
        ICMP: 10, TCP: 3600, UDP: 30
      TCP Timeouts [sec]:
        SYN wait time: 30, FIN wait time: 1
      TCP Ageout Timeouts [sec]:
        SYN wait time: 30, FIN wait time: 1
      TCP RST pkt control:
        half-open: On, half-close: On, idle: On
      UDP Timeout [msec]:
        UDP Half-open time: 30000
      UDP Ageout Timeout [msec]:
        UDP Half-open time: 30000
       
      Max Sessions: Unlimited
      Number of Simultaneous Packet per Sessions: 0
      Syn Cookie and Resource Management:
        Global Syn Flood Limit: 4294967295
        Global Total Session : 4294967295
        Global Number of Simultaneous Packet per Session : 
      Global Total Session Aggressive Aging Disabled
      Global alert : Off
      Global max incomplete : 4294967295
      Global max incomplete TCP: 4294967295
      Global max incomplete UDP: 4294967295
      Global max incomplete ICMP: 4294967295
      Global max incomplete Aggressive Aging Disabled
      Per Box Configuration
        syn flood limit : 4294967295
        Total Session Aggressive Aging Disabled
        max incomplete : 4294967295
        max incomplete TCP: 4294967295
        max incomplete UDP: 4294967295
        max incomplete ICMP: 4294967295
        max incomplete Aggressive Aging Disabled
  Inspect Parameter Map: vrf-default
  Parameter Map Type: VRF-Parameter-Map
  VRF PMAP syn flood limit : 4294967295
  VRF PMAP total session : 4294967295
  VRF PMAP total session Aggressive Aging Disabled
  VRF PMAP alert : Off
  VRF PMAP max incomplete : 4294967295
  VRF PMAP max incomplete TCP: 4294967295
  VRF PMAP max incomplete UDP: 4294967295
  VRF PMAP max incomplete ICMP: 4294967295
  VRF PMAP max incomplete Aggressive Aging Disabled
--show platform software firewall FP active zones--
Forwarding Manager Firewall Zone Configurations
  Zone Name: service, parameter-map: (null), Obj-id 65534
  Zone Name: self, parameter-map: (null), Obj-id 65535
--show platform software firewall RP active zones--
Forwarding Manager Firewall Zone Configurations
  Zone Name: self, parameter-map: 
  Zone Name: service, parameter-map:''',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_show_policy_firewall_config_platform(self.device)
        self.assertIn(
            'show policy-firewall config platform',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show policy-firewall config platform']
        self.assertEqual(result, expected_output)

    def test_execute_show_policy_firewall_config_platform_with_filter(self):
        self.device = Mock()
        filtered_output = '''--show platform software firewall FP active parameter-maps--
Forwarding Manager Inspect Parameter-Maps
  Inspect Parameter Map: global, Index 1
  Parameter Map Type: Parameter-Map
      Global Parameter-Map'''

        results_map = {
            'show policy-firewall config platform | include Parameter': filtered_output,
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_show_policy_firewall_config_platform(self.device, filter_option="include Parameter")
        self.assertIn(
            'show policy-firewall config platform | include Parameter',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = filtered_output
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    import unittest
    unittest.main()