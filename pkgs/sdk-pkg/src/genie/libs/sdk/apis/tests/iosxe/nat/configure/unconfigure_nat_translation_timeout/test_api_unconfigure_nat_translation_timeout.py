from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_translation_timeout

class TestUnconfigureNatTranslationTimeout(TestCase):

    def test_unconfigure_nat_translation_timeout(self):
        device = Mock()
        result = unconfigure_nat_translation_timeout(device, 'udp-timeout')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat translation udp-timeout'],)
        )