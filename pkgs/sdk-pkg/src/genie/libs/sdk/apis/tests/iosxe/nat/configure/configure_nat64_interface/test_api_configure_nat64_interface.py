from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_interface

class TestConfigureNat64Interface(TestCase):

    def test_configure_nat64_interface(self):
        device = Mock()
        result = configure_nat64_interface(device, 'TwentyFiveGigE2/0/9')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE2/0/9','nat64 enable'],)
        )