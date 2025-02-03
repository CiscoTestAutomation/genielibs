from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_interface_rep_ztp
from unittest.mock import Mock


class TestConfigureInterfaceRepZtp(TestCase):

    def test_configure_interface_rep_ztp(self):
        self.device = Mock()
        result = configure_interface_rep_ztp(self.device, ['GigabitEthernet1/0/1'], 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'switchport mode trunk', 'rep segment 1', 'rep ztp-enable'],)
        )
