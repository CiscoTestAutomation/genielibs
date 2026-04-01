from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv4_object_group

class TestUnconfigureIpv4ObjectGroup(TestCase):

    def test_unconfigure_ipv4_object_group(self):
        device = Mock()
        result = unconfigure_ipv4_object_group(device, 'ogacl_network_P1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no object-group network ogacl_network_P1'],)
        )