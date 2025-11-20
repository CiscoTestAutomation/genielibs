from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_default_source
from unittest.mock import Mock


class TestConfigureCtsSxpDefaultSource(TestCase):

    def test_configure_cts_sxp_default_source(self):
        self.device = Mock()
        result = configure_cts_sxp_default_source(self.device, '1.1.1.1', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp default source-ip 1.1.1.1'],)
        )
