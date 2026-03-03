from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_disable_nat_scale

class TestConfigureDisableNatScale(TestCase):

    def test_configure_disable_nat_scale(self):
        device = Mock()
        result = configure_disable_nat_scale(device, True, False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat create flow-entries'],)
        )