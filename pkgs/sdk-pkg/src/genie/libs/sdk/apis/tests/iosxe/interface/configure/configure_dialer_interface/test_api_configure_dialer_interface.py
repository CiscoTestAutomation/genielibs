from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_dialer_interface
from unittest.mock import Mock


class TestConfigureDialerInterface(TestCase):

    def test_configure_dialer_interface(self):
        self.device = Mock()
        result = configure_dialer_interface(self.device, 'Dialer10', 'ppp', 'chap', 'negotiated', '10', None, None, None, None, None, False, True, True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Dialer10', 'encapsulation ppp', 'no shutdown', 'dialer pool 10', 'ip address negotiated', 'ppp authentication chap callin', 'dialer down-with-vInterface', 'ppp mtu adaptive', 'ppp ipcp address required'],)
        )
