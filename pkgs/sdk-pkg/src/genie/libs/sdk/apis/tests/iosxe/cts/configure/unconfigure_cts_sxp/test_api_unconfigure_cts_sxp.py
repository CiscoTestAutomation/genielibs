from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp
from unittest.mock import Mock


class TestUnconfigureCtsSxp(TestCase):

    def test_unconfigure_cts_sxp(self):
        self.device = Mock()
        result = unconfigure_cts_sxp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp enable'],)
        )
