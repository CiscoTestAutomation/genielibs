from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t101_serial_channel
from unittest.mock import Mock


class TestUnconfigureScadaT101SerialChannel(TestCase):

    def test_unconfigure_scada_t101_serial_channel(self):
        self.device = Mock()
        result = unconfigure_scada_t101_serial_channel(self.device, 't101_serial_channel_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'no channel t101_serial_channel_1'],)
        )
