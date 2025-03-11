from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t101_serial_session
from unittest.mock import Mock


class TestConfigureScadaT101SerialSession(TestCase):

    def test_configure_scada_t101_serial_session(self):
        self.device = Mock()
        result = configure_scada_t101_serial_session(self.device, 't101_serial_session_1', 't101_serial_channel_1', 'two', 'one', 'two', 3)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'session t101_serial_session_1', 'attach-to-channel t101_serial_channel_1', 'common-addr-size two', 'cot-size one', 'info-obj-addr-size two', 'link-addr 3'],)
        )
