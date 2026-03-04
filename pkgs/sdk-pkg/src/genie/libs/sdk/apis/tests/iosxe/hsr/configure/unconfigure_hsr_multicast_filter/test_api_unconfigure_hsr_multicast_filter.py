from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hsr.configure import unconfigure_hsr_multicast_filter
from unittest.mock import Mock


class TestUnconfigureHsrMulticastFilter(TestCase):

    def test_unconfigure_hsr_multicast_filter(self):
        self.device = Mock()
        result = unconfigure_hsr_multicast_filter(self.device, 1, 5, '0000.0000.0011', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no hsr-ring 1 multicast_filter_deny_group 5 0000.0000.0011',)
        )
