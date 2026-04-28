from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_bridge_domain


class TestConfigureBridgeDomain(TestCase):

    def test_configure_bridge_domain(self):
        device = Mock()
        result = configure_bridge_domain(
            device,
            '50'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['bridge-domain 50'],)
        )