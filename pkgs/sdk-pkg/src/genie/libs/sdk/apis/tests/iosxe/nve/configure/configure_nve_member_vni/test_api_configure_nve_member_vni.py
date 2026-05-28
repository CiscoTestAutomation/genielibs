from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.nve.configure import configure_nve_member_vni


class TestConfigureNveMemberVni(TestCase):

    def test_configure_nve_member_vni(self):
        self.device = Mock()
        configure_nve_member_vni(
            self.device, 'nve1', '11111', '33.33.33.33', 'Loopback11'
        )
        self.device.configure.assert_called_once_with([
            "interface nve1",
            "member vni 11111",
            "ingress-replication 33.33.33.33",
            "source-interface Loopback11",
        ])

    def test_configure_nve_member_vni_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_nve_member_vni(
                self.device, 'nve1', '11111', '33.33.33.33', 'Loopback11'
            )
