from unittest import TestCase
from genie.libs.sdk.apis.iosxe.SVI.configure import configure_SVI_Unnumbered
from unittest.mock import Mock


class TestConfigureSviUnnumbered(TestCase):

    def test_configure_SVI_Unnumbered(self):
        self.device = Mock()
        configure_SVI_Unnumbered(self.device, 'Vlan500', 'Loopback1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Vlan500', 'ip unnumbered Loopback1','ipv6 unnumbered Loopback1'],)
        )
