from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fqdn.configure import configure_fqdn_ttl_timeout_factor
from unittest.mock import Mock


class TestConfigureFqdnTtlTimeoutFactor(TestCase):

    def test_configure_fqdn_ttl_timeout_factor(self):
        self.device = Mock()
        result = configure_fqdn_ttl_timeout_factor(self.device, '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('fqdn ttl-timeout-factor 10',)
        )
