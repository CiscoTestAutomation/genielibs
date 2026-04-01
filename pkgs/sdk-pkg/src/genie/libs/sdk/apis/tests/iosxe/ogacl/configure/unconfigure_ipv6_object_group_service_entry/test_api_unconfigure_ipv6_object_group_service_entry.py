from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_object_group_service_entry


class TestUnconfigureIpv6ObjectGroupServiceEntry(TestCase):

    def test_unconfigure_ipv6_object_group_service_entry(self):
        device = Mock()
        result = unconfigure_ipv6_object_group_service_entry(
            device=device,
            og_name='v6-serv-all',
            ipv6_service='tcp-udp eq 5000'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['object-group v6-service v6-serv-all', 'no tcp-udp eq 5000'],)
        )