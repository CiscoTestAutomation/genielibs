from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_dnp3_serial_session
from unittest.mock import Mock


class TestConfigureScadaDnp3SerialSession(TestCase):

    def test_configure_scada_dnp3_serial_session(self):
        self.device = Mock()
        result = configure_scada_dnp3_serial_session(self.device, 'dnp3_serial_session_1', 'dnp3_serial_channel_1', 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol dnp3-serial', 'session dnp3_serial_session_1', 'attach-to-channel dnp3_serial_channel_1', 'link-addr dest 1'],)
        )
