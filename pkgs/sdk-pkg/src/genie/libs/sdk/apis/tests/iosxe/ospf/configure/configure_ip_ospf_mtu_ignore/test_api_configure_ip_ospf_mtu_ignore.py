from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ip_ospf_mtu_ignore


class TestConfigureIpOspfMtuIgnore(TestCase):

    def test_configure_ip_ospf_mtu_ignore(self):
        device = Mock()
        result = configure_ip_ospf_mtu_ignore(
            device,
            'Vlan1001'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Vlan1001', 'ip ospf mtu-ignore'],)
        )