from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_connection
from unittest.mock import Mock


class TestConfigureCtsSxpConnection(TestCase):

    def test_configure_cts_sxp_connection(self):
        self.device = Mock()
        result = configure_cts_sxp_connection(self.device, '70.70.70.1', 'both')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp connection peer 70.70.70.1 password default mode local both'],)
        )
