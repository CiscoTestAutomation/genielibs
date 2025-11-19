from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fips.configure import configure_dynamic_cmap
from unittest.mock import Mock


class TestConfigureDynamicCmap(TestCase):

    def test_configure_dynamic_cmap(self):
        self.device = Mock()
        result = configure_dynamic_cmap(self.device, 'myVpnMap', 'myTransformSet', 'myDynamicMap', 10, None, None, False, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto dynamic-map myDynamicMap 10', 'set transform-set myTransformSet', 'crypto map myVpnMap 10 ipsec-isakmp dynamic myDynamicMap'],)
        )
