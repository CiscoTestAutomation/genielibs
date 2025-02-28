from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_dnp3_serial_channel
from unittest.mock import Mock


class TestConfigureScadaDnp3SerialChannel(TestCase):

    def test_configure_scada_dnp3_serial_channel(self):
        self.device = Mock()
        result = configure_scada_dnp3_serial_channel(self.device, 'dnp3_serial_channel_1', 5, 60, 'Async 0/3/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol dnp3-serial', 'channel dnp3_serial_channel_1', 'link-addr source 5', 'request-timeout 60', 'bind-to-interface Async 0/3/0'],)
        )
