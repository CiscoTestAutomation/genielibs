from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.execute import (
    execute_clear_l2tp_all,
    execute_clear_vpdn_counters,
    execute_clear_vpdn_counters_session_id,
    execute_clear_vpdn_counters_session_interface_virtual_access,
    execute_clear_vpdn_counters_session_username,
    execute_clear_vpdn_counters_tunnel_all,
    execute_clear_vpdn_counters_tunnel_hostname,
    execute_clear_vpdn_counters_tunnel_id,
    execute_clear_vpdn_counters_tunnel_ip,
    execute_clear_vpdn_dead_cache_all,
    execute_clear_vpdn_dead_cache_group,
    execute_clear_vpdn_dead_cache_ip_address,
    execute_clear_vpdn_history_failure,
    execute_clear_vpdn_tunnel_l2tp_all,
    execute_clear_vpdn_tunnel_pptp,
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

    def test_execute_clear_vpdn_tunnel_pptp(self):
        device = Mock()

        result = execute_clear_vpdn_tunnel_pptp(device, "remote1", "local1")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn tunnel pptp remote1 local1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters(self):
        device = Mock()

        result = execute_clear_vpdn_counters(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_tunnel_all(self):
        device = Mock()

        result = execute_clear_vpdn_counters_tunnel_all(device, "l2tp")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters tunnel l2tp all",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_tunnel_id(self):
        device = Mock()

        result = execute_clear_vpdn_counters_tunnel_id(device, "l2tp", "123")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters tunnel l2tp id 123",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_tunnel_hostname(self):
        device = Mock()

        result = execute_clear_vpdn_counters_tunnel_hostname(
            device, "pptp", "remote1", "local1"
        )

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters tunnel pptp hostname remote1 local1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_tunnel_ip(self):
        device = Mock()

        result = execute_clear_vpdn_counters_tunnel_ip(
            device, "l2tp", "local", "10.1.1.1"
        )

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters tunnel l2tp ip local 10.1.1.1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_session_username(self):
        device = Mock()

        result = execute_clear_vpdn_counters_session_username(
            device, "user1"
        )

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters session username user1",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_session_id(self):
        device = Mock()

        result = execute_clear_vpdn_counters_session_id(
            device, "123", "456"
        )

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters session id 123 456",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_counters_session_interface_virtual_access(
        self,
    ):
        device = Mock()

        result = execute_clear_vpdn_counters_session_interface_virtual_access(
            device, "1.2"
        )

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn counters session interface virtual-access 1.2",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_vpdn_history_failure(self):
        device = Mock()

        result = execute_clear_vpdn_history_failure(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear vpdn history failure",
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
