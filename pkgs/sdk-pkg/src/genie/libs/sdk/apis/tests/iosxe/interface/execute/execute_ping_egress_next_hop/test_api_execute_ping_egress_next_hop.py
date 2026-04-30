from unittest import TestCase
from unittest.mock import Mock, patch

with patch("pwd.getpwuid", return_value=("codex", "", 0, 0, "", "", "")):
    from genie.libs.sdk.apis.iosxe.interface.execute import (
        execute_ping_egress_next_hop,
    )


class TestExecutePingEgressNextHop(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "9350-2M"
        self.device.execute.return_value = "Success rate is 100 percent"

    def test_execute_ping_egress_next_hop_vlan(self):
        result = execute_ping_egress_next_hop(
            self.device,
            address="2.2.2.2",
            next_hop="102.1.1.2",
            egress_value="200",
            egress_type="vlan",
            timeout=30,
        )
        self.device.execute.assert_called_with(
            "ping 2.2.2.2 egress vlan 200 next-hop 102.1.1.2",
            timeout=30,
        )
        self.assertIn("Success rate is 100 percent", result)

    def test_execute_ping_egress_next_hop_interface(self):
        result = execute_ping_egress_next_hop(
            self.device,
            address="2.2.2.2",
            next_hop="102.1.1.2",
            egress_value="GigabitEthernet1/0/33",
            timeout=30,
        )
        self.device.execute.assert_called_with(
            "ping 2.2.2.2 egress GigabitEthernet1/0/33 next-hop 102.1.1.2",
            timeout=30,
        )
        self.assertIn("Success rate is 100 percent", result)
