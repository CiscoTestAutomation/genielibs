from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_enable_nat_scale

class TestConfigureEnableNatScale(TestCase):

    def test_configure_enable_nat_scale(self):
        device = Mock()
        result = configure_enable_nat_scale(device, 60, True, False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat create flow-entries'],)
        )