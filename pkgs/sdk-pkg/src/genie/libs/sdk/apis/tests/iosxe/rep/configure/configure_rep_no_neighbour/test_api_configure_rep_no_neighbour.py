from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_rep_no_neighbour
from unittest.mock import Mock


class TestConfigureRepNoNeighbour(TestCase):

    def test_configure_rep_no_neighbour(self):
        self.device = Mock()
        result = configure_rep_no_neighbour(self.device, ['GigabitEthernet1/0/3'], '3', 'primary')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/3', 'switchport mode trunk', 'rep segment 3 edge no-neighbor primary', 'shut', 'no shut'],)
        )
