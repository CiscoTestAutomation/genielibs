from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_pim_on_interface
from unittest.mock import Mock


class TestConfigureIpv6PimOnInterface(TestCase):

    def test_configure_ipv6_pim_on_interface(self):
        self.device = Mock()
        result = configure_ipv6_pim_on_interface(self.device, 'FortyGigabitEthernet1/0/9')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface FortyGigabitEthernet1/0/9', 'ipv6 pim', 'end'],)
        )
