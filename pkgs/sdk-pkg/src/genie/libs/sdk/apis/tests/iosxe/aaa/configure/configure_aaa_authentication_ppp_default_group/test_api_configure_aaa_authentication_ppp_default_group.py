from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.configure import (
    configure_aaa_authentication_ppp_default_group,
)


class TestConfigureAaaAuthenticationPppDefaultGroup(TestCase):

    def test_configure_aaa_authentication_ppp_default_group_radius(self):
        self.device = Mock()
        configure_aaa_authentication_ppp_default_group(self.device, 'radius')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authentication ppp default group radius',)
        )
