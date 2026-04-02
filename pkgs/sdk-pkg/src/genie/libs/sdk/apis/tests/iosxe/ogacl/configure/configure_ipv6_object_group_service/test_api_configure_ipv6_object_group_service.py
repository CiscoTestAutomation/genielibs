from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv6_object_group_service

class TestConfigureIpv6ObjectGroupService(TestCase):

    def test_configure_ipv6_object_group_service(self):
        device = Mock()
        result = configure_ipv6_object_group_service(
            device=device,
            og_name='v6-serv-all',
            ipv6_service='tcp-udp eq 5000'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['object-group v6-service v6-serv-all', 'tcp-udp eq 5000'],)
        )