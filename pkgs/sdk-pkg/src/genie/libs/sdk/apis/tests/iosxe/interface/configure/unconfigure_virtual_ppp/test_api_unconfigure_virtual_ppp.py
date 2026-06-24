from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_virtual_ppp
from unittest.mock import Mock


class TestUnconfigureVirtualPpp(TestCase):

    def test_unconfigure_virtual_ppp(self):
        self.device = Mock()
        result = unconfigure_virtual_ppp(self.device, 1, 'loopback1', 1436, 1272, 30, 'cisco', 'sisco', 'cisco', 'sisco', '2.2.2.2 113 encapsulation l2tpv2 pw-class PW_CLASS_011')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Virtual-PPP1', 'no ip unnumbered loopback1', 'no ip mtu 1436', 'no ip tcp adjust-mss 1272', 'no load-interval 30', 'no ppp chap hostname cisco', 'no ppp chap password sisco', 'no ppp pap sent-username cisco password sisco', 'no pseudowire 2.2.2.2 113 encapsulation l2tpv2 pw-class PW_CLASS_011'],)
        )
