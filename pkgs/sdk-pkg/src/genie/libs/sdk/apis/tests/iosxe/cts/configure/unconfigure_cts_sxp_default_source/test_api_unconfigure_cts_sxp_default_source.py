from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_default_source
from unittest.mock import Mock


class TestUnconfigureCtsSxpDefaultSource(TestCase):

    def test_unconfigure_cts_sxp_default_source(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_default_source(self.device, '1.1.1.1', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp default source-ip 1.1.1.1'],)
        )
