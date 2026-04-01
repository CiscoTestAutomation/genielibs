from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nve.configure import unconfig_nve_src_intf

class TestUnconfigNveSrcIntf(TestCase):

    def test_unconfig_nve_src_intf(self):
        device = Mock()
        result = unconfig_nve_src_intf(device, "nve 1")
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface nve 1', 'no source-interface'],)
        )