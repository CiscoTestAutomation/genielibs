from unittest import TestCase
from genie.libs.sdk.apis.iosxe.SVI.configure import configure_SVI_Autostate
from unittest.mock import Mock


class TestConfigureSviAutostate(TestCase):

    def test_configure_SVI_Autostate(self):
        self.device = Mock()
        configure_SVI_Autostate(self.device, 'Vlan500')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Vlan500', 'no autostate'],)
        )
