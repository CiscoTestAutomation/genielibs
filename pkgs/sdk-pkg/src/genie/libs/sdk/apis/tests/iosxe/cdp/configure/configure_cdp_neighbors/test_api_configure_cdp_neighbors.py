from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_neighbors

class TestConfigureCdpNeighbors(TestCase):

    def test_configure_cdp_neighbors(self):
        device = Mock()
        result = configure_cdp_neighbors(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cdp run'],)
        )