from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t101_serial_sector
from unittest.mock import Mock


class TestUnconfigureScadaT101SerialSector(TestCase):

    def test_unconfigure_scada_t101_serial_sector(self):
        self.device = Mock()
        result = unconfigure_scada_t101_serial_sector(self.device, 't101_serial_sector_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'no sector t101_serial_sector_1'],)
        )
