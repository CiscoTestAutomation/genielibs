from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp
from unittest.mock import Mock


class TestConfigureCtsSxp(TestCase):

    def test_configure_cts_sxp(self):
        self.device = Mock()
        result = configure_cts_sxp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp enable'],)
        )
