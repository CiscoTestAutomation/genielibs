from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t104_ip_sector
from unittest.mock import Mock


class TestConfigureScadaT104IpSector(TestCase):

    def test_configure_scada_t104_ip_sector(self):
        self.device = Mock()
        result = configure_scada_t104_ip_sector(self.device, 't104_ip_sector_1', 't104_ip_session_1', 3, 't101_serial_sector_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'sector t104_ip_sector_1', 'attach-to-session t104_ip_session_1', 'asdu-addr 3', 'map-to-sector t101_serial_sector_1'],)
        )
