from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import (
    unconfigure_ipv6_flow_monitor_on_interface,
)


class TestUnconfigureIpv6FlowMonitorOnInterface(TestCase):

    def test_unconfigure_ipv6_flow_monitor_on_interface(self):
        self.device = Mock()
        result = unconfigure_ipv6_flow_monitor_on_interface(
            self.device, 'po10', 'mon1', 'sampler_random', 'input'
        )
        self.assertIsNone(result)
        self.device.configure.assert_called_once_with([
            'interface po10',
            'no ipv6 flow monitor mon1 sampler sampler_random input'
        ])
