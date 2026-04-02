from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_object_group_network

class TestConfigureIpv4ObjectGroupNetwork(TestCase):

    def test_configure_ipv4_object_group_network(self):
        device = Mock()
        result = configure_ipv4_object_group_network(
            device, 'ogacl_network_P1', 'IXIA_P1', '20.20.20.1', '255.255.255.0'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'object-group network ogacl_network_P1',
                'description IXIA_P1',
                '20.20.20.1 255.255.255.0'
            ],)
        )