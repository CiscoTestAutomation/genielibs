from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_translation_timeout

class TestUnconfigureNat64TranslationTimeout(TestCase):

    def test_unconfigure_nat64_translation_timeout(self):
        device = Mock()
        result = unconfigure_nat64_translation_timeout(device, 'tcp', '')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no nat64 translation timeout tcp',)
        )