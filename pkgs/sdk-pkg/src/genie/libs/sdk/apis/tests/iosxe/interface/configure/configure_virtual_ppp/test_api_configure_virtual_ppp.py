from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_virtual_ppp
from unittest.mock import Mock


class TestConfigureVirtualPpp(TestCase):

    def test_configure_virtual_ppp(self):
        self.device = Mock()
        result = configure_virtual_ppp(self.device, 1, 'loopback1', 1436, 1272, 30, 'cisco', 'sisco', 'cisco', 'sisco', '2.2.2.2 113 encapsulation l2tpv2 pw-class PW_CLASS_011', 9)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Virtual-PPP1', 'ip unnumbered loopback1', 'ip mtu 1436', 'ip tcp adjust-mss 1272', 'load-interval 30', 'ppp chap hostname cisco', 'ppp chap password 9 sisco', 'ppp pap sent-username cisco password sisco', 'pseudowire 2.2.2.2 113 encapsulation l2tpv2 pw-class PW_CLASS_011'],)
        )
