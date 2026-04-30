from unittest import TestCase
from genie.libs.sdk.apis.iosxe.live_protect.configure import unconfigure_platform_security_live_protect_shield_enforcing
from unittest.mock import Mock


class TestUnconfigurePlatformSecurityLiveProtectShieldEnforcing(TestCase):

    def test_unconfigure_platform_security_live_protect_shield_enforcing(self):
        self.device = Mock()
        result = unconfigure_platform_security_live_protect_shield_enforcing(self.device, 'cve-2026-20000-v01')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no platform security live-protect shield cve-2026-20000-v01 enforcing',)
        )
