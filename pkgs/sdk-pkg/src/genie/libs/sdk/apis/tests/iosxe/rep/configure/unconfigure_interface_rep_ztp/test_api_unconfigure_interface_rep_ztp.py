from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_interface_rep_ztp
from unittest.mock import Mock


class TestUnconfigureInterfaceRepZtp(TestCase):

    def test_unconfigure_interface_rep_ztp(self):
        self.device = Mock()
        result = unconfigure_interface_rep_ztp(self.device, ['GigabitEthernet1/0/1'], 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'no rep segment 1', 'no rep ztp-enable', 'no switchport mode trunk'],)
        )
