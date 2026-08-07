import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_router_isis


class TestConfigureRouterIsis(TestCase):

    def test_configure_router_isis(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_router_isis(
            device,
            "test",
            "49.1290.0000.0011.00",
            "Gi1/0/4",
            "wide",
            "Gi1/0/4",
            "level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis test",
                "net 49.1290.0000.0011.00",
                "router-id Gi1/0/4",
                "metric-style wide",
                "mpls traffic-eng router-id Gi1/0/4",
                "mpls traffic-eng level-1",
            ],
        )

    def test_configure_router_isis_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_router_isis(
            device,
            "test",
            None,
            "Gi1/0/4",
            "wide",
            "Gi1/0/4",
            "level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis test",
                "router-id Gi1/0/4",
                "metric-style wide",
                "mpls traffic-eng router-id Gi1/0/4",
                "mpls traffic-eng level-1",
            ],
        )

    def test_configure_router_isis_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_router_isis(
            device,
            "test",
            None,
            None,
            "wide",
            "Gi1/0/4",
            "level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis test",
                "metric-style wide",
                "mpls traffic-eng router-id Gi1/0/4",
                "mpls traffic-eng level-1",
            ],
        )

    def test_configure_router_isis_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_router_isis(
            device,
            "test",
            None,
            None,
            None,
            "Gi1/0/4",
            "level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis test",
                "mpls traffic-eng router-id Gi1/0/4",
                "mpls traffic-eng level-1",
            ],
        )

    def test_configure_router_isis_4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_router_isis(
            device,
            "test",
            None,
            None,
            None,
            None,
            "level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis test",
                "mpls traffic-eng level-1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
