import unittest
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_destination_and_get_output)


class TestConfigureLocalSpanDestinationAndGetOutput(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.configure.return_value = "  done  "

    def test_dest_no_options(self):
        result = configure_local_span_destination_and_get_output(
            self.device, 1, 'gi0/1/5')
        self.device.configure.assert_called_once_with(
            "monitor session 1 destination interface gi0/1/5")
        self.assertEqual(result, "done")

    def test_dest_encapsulation_only(self):
        configure_local_span_destination_and_get_output(
            self.device, 1, 'gi0/1/5', encapsulation='dot1q')
        self.device.configure.assert_called_once_with(
            "monitor session 1 destination interface gi0/1/5 "
            "encapsulation dot1q")

    def test_dest_encapsulation_with_ingress_dot1q_and_vlan(self):
        configure_local_span_destination_and_get_output(
            self.device, 1, 'gi0/1/5',
            encapsulation='replicate', ingress='dot1q', vlan_id=100)
        self.device.configure.assert_called_once_with(
            "monitor session 1 destination interface gi0/1/5 "
            "encapsulation replicate ingress dot1q vlan 100")

    def test_dest_encapsulation_with_ingress_vlan(self):
        configure_local_span_destination_and_get_output(
            self.device, 2, 'gi0/1/6',
            encapsulation='dot1q', ingress='vlan', vlan_id=200)
        self.device.configure.assert_called_once_with(
            "monitor session 2 destination interface gi0/1/6 "
            "encapsulation dot1q ingress vlan 200")

    def test_dest_no_encapsulation_with_ingress_untagged(self):
        configure_local_span_destination_and_get_output(
            self.device, 3, 'gi0/1/7',
            ingress='untagged', vlan_id=300)
        self.device.configure.assert_called_once_with(
            "monitor session 3 destination interface gi0/1/7 "
            "ingress untagged vlan 300")

    def test_dest_no_encapsulation_with_ingress_vlan(self):
        configure_local_span_destination_and_get_output(
            self.device, 4, 'gi0/1/8', ingress='vlan', vlan_id=400)
        self.device.configure.assert_called_once_with(
            "monitor session 4 destination interface gi0/1/8 "
            "ingress vlan 400")

    def test_dest_subcommand_failure(self):
        self.device.configure.side_effect = SubCommandFailure("boom")
        with self.assertRaises(SubCommandFailure):
            configure_local_span_destination_and_get_output(
                self.device, 1, 'gi0/1/5')


if __name__ == '__main__':
    unittest.main()
