from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fqdn.configure import unconfigure_fqdn_ttl_timeout_factor
from unittest.mock import Mock


class TestUnconfigureFqdnTtlTimeoutFactor(TestCase):

    def test_unconfigure_fqdn_ttl_timeout_factor(self):
        self.device = Mock()
        result = unconfigure_fqdn_ttl_timeout_factor(self.device, '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no fqdn ttl-timeout-factor 10',)
        )
