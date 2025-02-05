from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_flow_monitor_sampler
from unittest.mock import Mock


class TestConfigureIpv6FlowMonitorSampler(TestCase):

    def test_configure_ipv6_flow_monitor_sampler(self):
        self.device = Mock()
        result = configure_ipv6_flow_monitor_sampler(self.device, 'vlan100', 'm6', 's1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface vlan100', 'ipv6 flow monitor m6 sampler s1 input', 'end'],)
        )
