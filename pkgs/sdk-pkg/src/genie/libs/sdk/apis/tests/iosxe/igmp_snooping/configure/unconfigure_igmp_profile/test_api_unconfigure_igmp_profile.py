from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import unconfigure_igmp_profile
from unittest.mock import Mock


class TestUnconfigureIgmpProfile(TestCase):

    def test_unconfigure_igmp_profile(self):
        self.device = Mock()
        result = unconfigure_igmp_profile(self.device, '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip igmp profile 10'],)
        )
