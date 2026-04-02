from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_object_group_service


class TestUnconfigureIpv6ObjectGroupService(TestCase):

    def test_unconfigure_ipv6_object_group_service(self):
        device = Mock()
        result = unconfigure_ipv6_object_group_service(
            device=device,
            og_name='v6-serv-all'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no object-group v6-service v6-serv-all',)
        )