from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_igmp_version

class TestUnconfigureIgmpVersion(TestCase):

    def test_unconfigure_igmp_version(self):
        device = Mock()
        result = unconfigure_igmp_version(device, 'loopback3001', '3')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('interface loopback3001\n no ip igmp version 3',)
        )