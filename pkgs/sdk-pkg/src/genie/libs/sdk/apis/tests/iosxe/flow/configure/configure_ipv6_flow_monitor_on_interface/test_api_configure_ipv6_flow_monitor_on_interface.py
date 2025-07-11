from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_ipv6_flow_monitor_on_interface
from unittest.mock import Mock


class TestConfigureIpv6FlowMonitorOnInterface(TestCase):

    def test_configure_ipv6_flow_monitor_on_interface(self):
        self.device = Mock()
        result = configure_ipv6_flow_monitor_on_interface(self.device, 'Te3/1/2', 'm6out', 'sampler_random', 'output')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Te3/1/2', 'ipv6 flow monitor m6out sampler sampler_random output'],)
        )
