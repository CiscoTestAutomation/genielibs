import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_dialer_interface


class TestConfigureDialerInterface(TestCase):

    def test_configure_dialer_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dialer_interface(
            device,
            "Dialer10",
            "ppp",
            "chap",
            "negotiated",
            "10",
            None,
            None,
            None,
            None,
            None,
            False,
            True,
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Dialer10", sent_commands)
        self.assertIn("encapsulation ppp", sent_commands)
        self.assertIn("no shutdown", sent_commands)
        self.assertIn("dialer pool 10", sent_commands)
        self.assertIn("ip address negotiated", sent_commands)
        self.assertIn("ppp authentication chap callin", sent_commands)
        self.assertIn("dialer down-with-vInterface", sent_commands)
        self.assertIn("ppp mtu adaptive", sent_commands)
        self.assertIn("ppp ipcp address required", sent_commands)

    def test_configure_dialer_interface_vpdn_without_callin(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dialer_interface(
            device,
            "Dialer1",
            "ppp",
            "chap",
            pool_num=1,
            dialer_group=1,
            ip_unnumbered="Loopback0",
            remote_name="lac",
            dialer_string="5550100",
            dialer_vpdn=True,
            authentication_callin=False,
        )

        expected_commands = [
            "interface Dialer1",
            "ip unnumbered Loopback0",
            "encapsulation ppp",
            "no shutdown",
            "dialer remote-name lac",
            "dialer string 5550100",
            "dialer vpdn",
            "dialer pool 1",
            "ppp authentication chap",
            "dialer-group 1",
        ]

        self.assertIsNone(result)
        self.assertEqual(device.configure.call_args.args[0], expected_commands)

    def test_configure_dialer_interface_inband_aaa_without_callin(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dialer_interface(
            device,
            "Dialer3",
            "ppp",
            "chap",
            dialer_group=3,
            ip_unnumbered="Loopback0",
            dialer_in_band=True,
            dialer_aaa=True,
            authentication_callin=False,
        )

        expected_commands = [
            "interface Dialer3",
            "ip unnumbered Loopback0",
            "encapsulation ppp",
            "no shutdown",
            "dialer in-band",
            "dialer aaa",
            "ppp authentication chap",
            "dialer-group 3",
        ]

        self.assertIsNone(result)
        self.assertEqual(device.configure.call_args.args[0], expected_commands)


if __name__ == "__main__":
    unittest.main()
