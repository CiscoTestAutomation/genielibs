from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.execute import (
    execute_clear_l2tp_all,
    execute_clear_vpdn_dead_cache_all,
    execute_clear_vpdn_dead_cache_group,
    execute_clear_vpdn_dead_cache_ip_address,
    execute_clear_vpdn_tunnel_l2tp_all,
)


class TestExecuteClearVpdnCommands(TestCase):

    def test_execute_clear_vpdn_dead_cache_all(self):
        device = Mock()

        result = execute_clear_vpdn_dead_cache_all(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn dead-cache all",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_dead_cache_ip_address(self):
        device = Mock()

        result = execute_clear_vpdn_dead_cache_ip_address(device, "10.1.1.1")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn dead-cache ip-address 10.1.1.1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_dead_cache_group(self):
        device = Mock()

        result = execute_clear_vpdn_dead_cache_group(device, "group1")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn dead-cache group group1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_tunnel_l2tp_all(self):
        device = Mock()

        result = execute_clear_vpdn_tunnel_l2tp_all(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn tunnel l2tp all",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_l2tp_all(self):
        device = Mock()

        result = execute_clear_l2tp_all(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear l2tp all",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)
