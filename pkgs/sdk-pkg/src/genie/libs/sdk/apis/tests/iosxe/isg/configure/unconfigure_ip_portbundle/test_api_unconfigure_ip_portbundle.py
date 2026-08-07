from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import unconfigure_ip_portbundle


class TestUnconfigureIpPortbundle(TestCase):

    def test_unconfigure_ip_portbundle(self):
        self.device = Mock()
        unconfigure_ip_portbundle(self.device)
        self.device.configure.assert_called_once_with("no ip portbundle")

    def test_unconfigure_ip_portbundle_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_ip_portbundle(self.device)
