from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_flow_monitor_sampler
from unittest.mock import Mock


class TestConfigureIpv6FlowMonitorSampler(TestCase):

    def test_configure_ipv6_flow_monitor_sampler(self):
        self.device = Mock()
        result = configure_ipv6_flow_monitor_sampler(self.device, 'Port-channel10', 'input', 'ipv6_monitor_in', 'sampler_random')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Port-channel10', 'ipv6 flow monitor ipv6_monitor_in sampler sampler_random input', 'end'],)
        )
