from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv4_object_group_service

class TestUnconfigureIpv4ObjectGroupService(TestCase):

    def test_unconfigure_ipv4_object_group_service(self):
        device = Mock()
        result = unconfigure_ipv4_object_group_service(device, 'ogacl_service')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no object-group service ogacl_service',)
        )