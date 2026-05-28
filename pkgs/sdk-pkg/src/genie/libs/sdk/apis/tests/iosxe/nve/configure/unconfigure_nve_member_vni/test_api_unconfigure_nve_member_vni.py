from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.nve.configure import unconfigure_nve_member_vni


class TestUnconfigureNveMemberVni(TestCase):

    def test_unconfigure_nve_member_vni(self):
        self.device = Mock()
        unconfigure_nve_member_vni(self.device, 'nve1', '11111', 'Loopback11')
        self.device.configure.assert_called_once_with([
            "interface nve1",
            "no member vni 11111",
            "no source-interface Loopback11",
        ])

    def test_unconfigure_nve_member_vni_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_nve_member_vni(self.device, 'nve1', '11111', 'Loopback11')
