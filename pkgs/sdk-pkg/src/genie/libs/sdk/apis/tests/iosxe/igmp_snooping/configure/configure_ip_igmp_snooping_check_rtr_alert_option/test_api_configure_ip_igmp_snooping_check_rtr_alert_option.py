import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    configure_ip_igmp_snooping_check_rtr_alert_option,
)


class TestConfigureIpIgmpSnoopingCheckRtrAlertOption(TestCase):

    def test_configure_ip_igmp_snooping_check_rtr_alert_option(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_check_rtr_alert_option(
            device,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping check rtr-alert-option")

    def test_configure_ip_igmp_snooping_check_rtr_alert_option_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_check_rtr_alert_option(
            device,
            vlan="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping vlan 20 check rtr-alert-option")


if __name__ == "__main__":
    unittest.main()
