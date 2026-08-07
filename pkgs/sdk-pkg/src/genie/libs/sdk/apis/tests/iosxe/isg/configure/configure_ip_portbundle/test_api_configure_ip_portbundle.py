from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import configure_ip_portbundle


class TestConfigureIpPortbundle(TestCase):

    def test_configure_ip_portbundle(self):
        self.device = Mock()
        configure_ip_portbundle(self.device)
        self.device.configure.assert_called_once_with(["ip portbundle"])

    def test_configure_ip_portbundle_with_length_and_source(self):
        self.device = Mock()
        configure_ip_portbundle(self.device, length=0, source='Loopback3')
        self.device.configure.assert_called_once_with(
            [
                "ip portbundle",
                "length 0",
                "source Loopback3",
            ]
        )

    def test_configure_ip_portbundle_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ip_portbundle(self.device)
