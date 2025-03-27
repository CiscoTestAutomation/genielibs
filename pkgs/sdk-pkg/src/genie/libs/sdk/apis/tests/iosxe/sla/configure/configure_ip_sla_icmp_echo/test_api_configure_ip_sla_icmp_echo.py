from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sla.configure import configure_ip_sla_icmp_echo
from unittest.mock import Mock


class TestConfigureIpSlaIcmpEcho(TestCase):

    def test_configure_ip_sla_icmp_echo(self):
        self.device = Mock()
        result = configure_ip_sla_icmp_echo(self.device, 2147483647, '3.4.2.1', None, None, None, None, 'Mgmt-vrf')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip sla 2147483647', 'icmp-echo 3.4.2.1', 'vrf Mgmt-vrf'],)
        )
