from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_translation_timeout

class TestConfigureNat64TranslationTimeout(TestCase):

    def test_configure_nat64_translation_timeout(self):
        device = Mock()
        result = configure_nat64_translation_timeout(device, 'tcp', 60)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['nat64 translation timeout tcp 60'],)
        )