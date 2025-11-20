from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpool_policy
from unittest.mock import Mock


class TestConfigureTrustpoolPolicy(TestCase):

    def test_configure_trustpool_policy(self):
        self.device = Mock()
        result = configure_trustpool_policy(self.device, 'GigabitEthernet0/0', None, 'http://10.106.29.252/ca-bundle.crt')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki trustpool policy', 'cabundle url http://10.106.29.252/ca-bundle.crt', 'source interface GigabitEthernet0/0'],)
        )
