from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_connection
from unittest.mock import Mock


class TestUnconfigureCtsSxpConnection(TestCase):

    def test_unconfigure_cts_sxp_connection(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_connection(self.device, '70.70.70.1', 'both')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp connection peer 70.70.70.1 password default mode local both'],)
        )
