from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_ipv6_flow_monitor_sampler
from unittest.mock import Mock


class TestUnconfigureIpv6FlowMonitorSampler(TestCase):

    def test_unconfigure_ipv6_flow_monitor_sampler(self):
        self.device = Mock()
        result = unconfigure_ipv6_flow_monitor_sampler(self.device, 'po10', 'input', 'ipv6_monitor_in', 'sampler_random')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface po10', 'no ipv6 flow monitor ipv6_monitor_in sampler sampler_random input', 'end'],)
        )
