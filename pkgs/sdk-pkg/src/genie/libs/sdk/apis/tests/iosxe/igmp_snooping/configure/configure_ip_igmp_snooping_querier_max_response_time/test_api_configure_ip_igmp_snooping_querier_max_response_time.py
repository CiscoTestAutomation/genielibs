import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    configure_ip_igmp_snooping_querier_max_response_time,
)


class TestConfigureIpIgmpSnoopingQuerierMaxResponseTime(TestCase):

    def test_configure_ip_igmp_snooping_querier_max_response_time(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_querier_max_response_time(
            device,
            10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping querier max-response-time 10")

    def test_configure_ip_igmp_snooping_querier_max_response_time_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_querier_max_response_time(
            device,
            10,
            vlan="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping vlan 20 querier max-response-time 10")


if __name__ == "__main__":
    unittest.main()
