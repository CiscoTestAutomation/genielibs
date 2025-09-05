from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_interface_rep_ztp
from unittest.mock import Mock


class TestUnconfigureInterfaceRepZtp(TestCase):

    def test_unconfigure_interface_rep_ztp(self):
        self.device = Mock()
        result = unconfigure_interface_rep_ztp(self.device, ['Gi1/6', 'Gi1/7'], '25')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/6', 'no rep segment 25', 'no rep ztp-enable', 'no switchport mode trunk'],)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (['interface Gi1/7', 'no rep segment 25', 'no rep ztp-enable', 'no switchport mode trunk'],)
        )
