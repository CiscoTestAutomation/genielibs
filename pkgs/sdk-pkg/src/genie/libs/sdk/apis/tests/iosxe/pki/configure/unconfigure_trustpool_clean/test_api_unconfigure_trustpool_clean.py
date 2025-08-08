from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_trustpool_clean
from unittest.mock import Mock


class TestUnconfigureTrustpoolClean(TestCase):

    def test_unconfigure_trustpool_clean(self):
        self.device = Mock()
        result = unconfigure_trustpool_clean(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto pki trustpool clean'],)
        )
