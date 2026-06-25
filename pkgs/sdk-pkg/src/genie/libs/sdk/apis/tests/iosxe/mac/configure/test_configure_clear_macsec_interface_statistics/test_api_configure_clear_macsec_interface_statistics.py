from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import configure_clear_macsec_interface_statistics


class TestConfigureClearMacsecInterfaceStatistics(TestCase):

    def test_configure_clear_macsec_interface_statistics(self):
        self.device = Mock()
        configure_clear_macsec_interface_statistics(self.device, intf='GigabitEthernet1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('clear macsec statistics interface GigabitEthernet1',)
        )
