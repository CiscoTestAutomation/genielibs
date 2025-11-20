from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_trustpool_policy
from unittest.mock import Mock


class TestUnconfigureTrustpoolPolicy(TestCase):

    def test_unconfigure_trustpool_policy(self):
        self.device = Mock()
        result = unconfigure_trustpool_policy(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto pki trustpool policy'],)
        )
