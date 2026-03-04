from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hsr.configure import configure_hsr_multicast_filter
from unittest.mock import Mock


class TestConfigureHsrMulticastFilter(TestCase):

    def test_configure_hsr_multicast_filter(self):
        self.device = Mock()
        result = configure_hsr_multicast_filter(self.device, 1, 5, '0000.0000.0011', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hsr-ring 1 multicast_filter_deny_group 5 0000.0000.0011',)
        )
