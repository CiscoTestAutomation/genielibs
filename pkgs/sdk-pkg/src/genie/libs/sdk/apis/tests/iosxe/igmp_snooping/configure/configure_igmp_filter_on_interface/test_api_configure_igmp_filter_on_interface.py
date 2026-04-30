from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import configure_igmp_filter_on_interface
from unittest.mock import Mock


class TestConfigureIgmpFilterOnInterface(TestCase):

    def test_configure_igmp_filter_on_interface(self):
        self.device = Mock()
        result = configure_igmp_filter_on_interface(self.device, 'fif1/0/9', '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface fif1/0/9', 'ip igmp filter 10'],)
        )
