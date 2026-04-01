from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_confederation_identifier
from unittest.mock import Mock


class TestConfigureBgpConfederationIdentifier(TestCase):

    def test_configure_bgp_confederation_identifier(self):
        self.device = Mock()
        result = configure_bgp_confederation_identifier(self.device, 50, 100)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 50', 'bgp confederation identifier 100', 'exit'],)
        )
