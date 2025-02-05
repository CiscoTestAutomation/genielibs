from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_fast_rep_segment
from unittest.mock import Mock


class TestUnconfigureFastRepSegment(TestCase):

    def test_unconfigure_fast_rep_segment(self):
        self.device = Mock()
        result = unconfigure_fast_rep_segment(self.device, ['GigabitEthernet1/0/1'], 1, 10, True, False, True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'no rep segment 1 edge', 'no rep fastmode', 'no switchport mode trunk', 'no shut', 'shut', 'no switchport trunk allowed vlan 10', 'no vlan 10'],)
        )
