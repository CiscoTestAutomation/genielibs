from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpool_clean
from unittest.mock import Mock


class TestConfigureTrustpoolClean(TestCase):

    def test_configure_trustpool_clean(self):
        self.device = Mock()
        result = configure_trustpool_clean(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki trustpool clean'],)
        )
