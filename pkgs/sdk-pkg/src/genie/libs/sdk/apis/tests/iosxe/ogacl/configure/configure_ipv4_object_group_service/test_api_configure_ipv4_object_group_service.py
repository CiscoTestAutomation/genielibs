from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_object_group_service

class TestConfigureIpv4ObjectGroupService(TestCase):

    def test_configure_ipv4_object_group_service(self):
        device = Mock()
        result = configure_ipv4_object_group_service(
            device,
            'ogacl_service',
            'services',
            ['ospf', 'icmp echo', 'icmp echo-reply', 'tcp source range 5000 6000']
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'object-group service ogacl_service',
                'description services',
                'ospf',
                'icmp echo',
                'icmp echo-reply',
                'tcp source range 5000 6000'
            ],)
        )