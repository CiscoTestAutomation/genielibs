from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_translation_timeout

class TestConfigureNatTranslationTimeout(TestCase):

    def test_configure_nat_translation_timeout(self):
        device = Mock()
        result = configure_nat_translation_timeout(device, 'udp-timeout', 120)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat translation udp-timeout 120'],)
        )