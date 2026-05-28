from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_show_policy_firewall_stats_platform
from unittest.mock import Mock


class TestExecuteShowPolicyFirewallStatsPlatform(TestCase):

    def test_execute_show_policy_firewall_stats_platform(self):
        self.device = Mock()
        results_map = {
            'show policy-firewall stats platform': '''--show platform software firewall FP active stats--
Firewall Platform Statistics:
  Total Session Count: 100
  Half-Open Session Count: 0
  Total Packets Inspected: 5000
  Total Packets Allowed: 4900
  Total Packets Dropped: 100
  TCP Sessions Active: 50
  UDP Sessions Active: 30
  ICMP Sessions Active: 20
  Total Bytes Inspected: 500000
  Total Bytes Allowed: 490000
  Total Bytes Dropped: 10000
--show platform software firewall RP active stats--
Firewall Platform Statistics:
  Total Session Count: 100
  Half-Open Session Count: 0
  Total Packets Inspected: 5000
  Total Packets Allowed: 4900
  Total Packets Dropped: 100
  TCP Sessions Active: 50
  UDP Sessions Active: 30
  ICMP Sessions Active: 20
  Total Bytes Inspected: 500000
  Total Bytes Allowed: 490000
  Total Bytes Dropped: 10000''',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_show_policy_firewall_stats_platform(self.device)
        self.assertIn(
            'show policy-firewall stats platform',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show policy-firewall stats platform']
        self.assertEqual(result, expected_output)

    def test_execute_show_policy_firewall_stats_platform_with_filter(self):
        self.device = Mock()
        filtered_output = '''  Total Session Count: 100
  TCP Sessions Active: 50
  UDP Sessions Active: 30
  ICMP Sessions Active: 20'''

        results_map = {
            'show policy-firewall stats platform | include Session': filtered_output,
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_show_policy_firewall_stats_platform(self.device, filter_option="include Session")
        self.assertIn(
            'show policy-firewall stats platform | include Session',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = filtered_output
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    import unittest
    unittest.main()
