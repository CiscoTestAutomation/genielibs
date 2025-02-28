from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t101_serial_session
from unittest.mock import Mock


class TestUnconfigureScadaT101SerialSession(TestCase):

    def test_unconfigure_scada_t101_serial_session(self):
        self.device = Mock()
        result = unconfigure_scada_t101_serial_session(self.device, 't101_serial_session_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t101', 'no session t101_serial_session_1'],)
        )
