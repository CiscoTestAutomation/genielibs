from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t101_serial_sector
from unittest.mock import Mock


class TestConfigureScadaT101SerialSector(TestCase):

    def test_configure_scada_t101_serial_sector(self):
        self.device = Mock()
        result = configure_scada_t101_serial_sector(self.device, 't101_serial_sector_1', 't101_serial_session_1', 3)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'sector t101_serial_sector_1', 'attach-to-session t101_serial_session_1', 'asdu-addr 3'],)
        )
