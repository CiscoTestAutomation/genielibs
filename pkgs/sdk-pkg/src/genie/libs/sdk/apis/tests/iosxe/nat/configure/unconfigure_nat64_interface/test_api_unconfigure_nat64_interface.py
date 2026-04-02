from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_interface

class TestUnconfigureNat64Interface(TestCase):

    def test_unconfigure_nat64_interface(self):
        device = Mock()
        result = unconfigure_nat64_interface(device, 'TwentyFiveGigE2/0/9')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE2/0/9', 'no nat64 enable'],)
        )