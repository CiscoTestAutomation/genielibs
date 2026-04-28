from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_trustpoint


class TestUnconfigureTrustpoint(TestCase):

    def test_unconfigure_trustpoint(self):
        device = Mock()
        result = unconfigure_trustpoint(
            device,
            'test'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no crypto pki trustpoint test',)
        )