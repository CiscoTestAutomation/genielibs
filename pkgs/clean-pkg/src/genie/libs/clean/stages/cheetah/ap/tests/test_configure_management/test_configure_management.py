import unittest
from unittest.mock import Mock, call, patch

from pyats.aetest.signals import TerminateStepSignal
from pyats.aetest.steps import Steps
from pyats.results import Failed, Passed

from genie.libs.clean.stages.cheetah.ap.stages import ConfigureManagement
from genie.libs.parser.cheetah.show_dhcp import ShowIpDhcpLease
from genie.libs.parser.cheetah.show_interface import ShowIpInterfaceBrief


ACTIVE_INTERFACE_OUTPUT = """\
Interface            IP-Address      Method   Status                 Protocol
Speed      Duplex
*wired0              192.0.2.10      DHCP     up                     up
1000       full
"""

DOWN_INTERFACE_OUTPUT = """\
Interface            IP-Address      Method   Status                 Protocol
Speed      Duplex
*wired1              n/a             n/a      down                   down
n/a        n/a
"""

NO_ADDRESS_OUTPUT = """\
Interface            IP-Address      Method   Status                 Protocol
Speed      Duplex
*wired0              n/a             n/a      up                     up
1000       full
"""

STATIC_INTERFACE_OUTPUT = """\
Interface            IP-Address      Method   Status                 Protocol
Speed      Duplex
*wired0              192.0.2.10      manual   up                     up
1000       full
"""

BOUND_LEASE_OUTPUT = """\
Interface wired0
 DHCP lease server: 192.0.2.1

vlan added_by active state disc_ago offer_ago req_ago ack_delay renew_at exp_at               ip          gw         bcast     dns mtu
   0        C   true bound   120       118       60       0.0012    30       90 192.0.2.10/24 192.0.2.1 192.0.2.255 0.0.0.0   0
"""

EXPIRED_LEASE_OUTPUT = """\
Interface wired0
 DHCP lease server: 192.0.2.1

vlan added_by active state disc_ago offer_ago req_ago ack_delay renew_at exp_at
              ip          gw         bcast     dns mtu
   0        C   false expired 120      118       60       0.0012    30       90
192.0.2.10/24 192.0.2.1 192.0.2.255 0.0.0.0   0
"""


class TestConfigureManagement(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureManagement()
        self.device = Mock()
        self.device.management = {}

    def test_check_management_interface_status_uses_active_interface(self):
        self.device.parse = Mock(
            return_value=ShowIpInterfaceBrief(device=self.device).cli(
                output=ACTIVE_INTERFACE_OUTPUT
            )
        )
        steps = Steps()

        self.cls.check_management_interface_status(
            device=self.device,
            steps=steps,
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.device.parse.assert_called_once_with("show ip interface brief")

    def test_check_management_interface_status_fails_without_address(self):
        self.device.parse = Mock(
            return_value=ShowIpInterfaceBrief(device=self.device).cli(
                output=NO_ADDRESS_OUTPUT
            )
        )
        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            self.cls.check_management_interface_status(
                device=self.device,
                steps=steps,
            )

        self.assertEqual(Failed, steps.details[0].result)
        self.assertEqual(
            "Management interface wired0 has no IPv4 address",
            steps.details[0].result.reason,
        )

    def test_check_management_interface_status_fails_without_dhcp(self):
        self.device.parse = Mock(
            return_value=ShowIpInterfaceBrief(device=self.device).cli(
                output=STATIC_INTERFACE_OUTPUT
            )
        )
        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            self.cls.check_management_interface_status(
                device=self.device,
                steps=steps,
            )

        self.assertEqual(Failed, steps.details[0].result)
        self.assertEqual(
            "Management interface wired0 is not using DHCP",
            steps.details[0].result.reason,
        )

    def test_check_management_interface_status_fails_when_active_interface_down(self):
        self.device.parse = Mock(
            return_value=ShowIpInterfaceBrief(device=self.device).cli(
                output=DOWN_INTERFACE_OUTPUT
            )
        )
        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            self.cls.check_management_interface_status(
                device=self.device,
                steps=steps,
            )

        self.assertEqual(Failed, steps.details[0].result)
        self.assertEqual(
            "Management interface wired1 is down",
            steps.details[0].result.reason,
        )

    def test_ping_gateway_uses_active_bound_lease(self):
        self.device.parse = Mock(
            return_value=ShowIpDhcpLease(device=self.device).cli(
                output=BOUND_LEASE_OUTPUT
            )
        )
        self.device.ping = Mock()
        steps = Steps()

        self.cls.ping_gateway(device=self.device, steps=steps)

        self.assertEqual(Passed, steps.details[-1].result)
        self.device.parse.assert_called_once_with("show ip dhcp lease")
        self.device.ping.assert_called_once_with(
            addr="192.0.2.1",
            source="wired0",
            timeout=120,
            count=5,
        )

    @patch("genie.libs.clean.stages.cheetah.ap.stages.time.sleep")
    def test_ping_gateway_retries(self, mock_sleep):
        self.device.parse = Mock(
            return_value=ShowIpDhcpLease(device=self.device).cli(
                output=BOUND_LEASE_OUTPUT
            )
        )
        self.device.ping = Mock(side_effect=[Exception("not ready"), None])
        steps = Steps()

        self.cls.ping_gateway(
            device=self.device,
            steps=steps,
            ping_attempts=2,
            ping_sleep=1,
        )

        self.assertEqual(Passed, steps.details[-1].result)
        self.assertEqual(
            [
                call(
                    addr="192.0.2.1",
                    source="wired0",
                    timeout=120,
                    count=5,
                ),
                call(
                    addr="192.0.2.1",
                    source="wired0",
                    timeout=120,
                    count=5,
                ),
            ],
            self.device.ping.call_args_list,
        )
        mock_sleep.assert_called_once_with(1)

    def test_ping_gateway_fails_without_active_bound_lease(self):
        self.device.parse = Mock(
            return_value=ShowIpDhcpLease(device=self.device).cli(
                output=EXPIRED_LEASE_OUTPUT
            )
        )
        self.device.ping = Mock()
        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            self.cls.ping_gateway(device=self.device, steps=steps)

        self.assertEqual(Failed, steps.details[0].result)
        self.assertEqual(
            "No active DHCP gateway found",
            steps.details[0].result.reason,
        )
        self.device.ping.assert_not_called()
