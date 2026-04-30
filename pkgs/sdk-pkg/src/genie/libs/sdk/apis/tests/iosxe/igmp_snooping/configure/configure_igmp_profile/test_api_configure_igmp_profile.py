from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import configure_igmp_profile
from unittest.mock import Mock


class TestConfigureIgmpProfile(TestCase):

    def test_configure_igmp_profile(self):
        self.device = Mock()
        result = configure_igmp_profile(self.device, '10', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip igmp profile 10'],)
        )
