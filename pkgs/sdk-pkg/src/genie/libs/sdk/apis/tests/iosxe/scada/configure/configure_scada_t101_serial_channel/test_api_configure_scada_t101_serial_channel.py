from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t101_serial_channel
from unittest.mock import Mock


class TestConfigureScadaT101SerialChannel(TestCase):

    def test_configure_scada_t101_serial_channel(self):
        self.device = Mock()
        result = configure_scada_t101_serial_channel(self.device, 't101_serial_channel_1', 'Async 0/2/0', 'balanced', 'one')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'channel t101_serial_channel_1', 'bind-to-interface Async 0/2/0', 'link-mode balanced', 'link-addr-size one'],)
        )
