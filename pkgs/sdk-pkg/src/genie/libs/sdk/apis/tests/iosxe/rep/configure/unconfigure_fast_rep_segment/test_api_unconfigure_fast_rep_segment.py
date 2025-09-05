from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_fast_rep_segment
from unittest.mock import Mock


class TestUnconfigureFastRepSegment(TestCase):

    def test_unconfigure_fast_rep_segment(self):
        self.device = Mock()
        result = unconfigure_fast_rep_segment(self.device, ['Gi1/6', 'Gi1/7'], '25', True, False, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/6', 'no rep segment 25', 'no rep fastmode', 'no switchport mode trunk', 'no shut', 'shut', 'no switchport trunk allowed vlan True', 'no vlan True'],)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (['interface Gi1/7', 'no rep segment 25', 'no rep fastmode', 'no switchport mode trunk', 'no shut', 'shut', 'no switchport trunk allowed vlan True', 'no vlan True'],)
        )
