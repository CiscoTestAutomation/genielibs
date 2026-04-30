from unittest import TestCase
from genie.libs.sdk.apis.iosxe.live_protect.configure import configure_platform_security_live_protect_shield_enforcing
from unittest.mock import Mock


class TestConfigurePlatformSecurityLiveProtectShieldEnforcing(TestCase):

    def test_configure_platform_security_live_protect_shield_enforcing(self):
        self.device = Mock()
        result = configure_platform_security_live_protect_shield_enforcing(self.device, 'cve-2026-20000-v01')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('platform security live-protect shield cve-2026-20000-v01 enforcing',)
        )
