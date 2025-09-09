from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_fast_rep_segment
from unittest.mock import Mock


class TestConfigureFastRepSegment(TestCase):

    def test_configure_fast_rep_segment(self):
        self.device = Mock()
        result = configure_fast_rep_segment(self.device, ['Gi1/6', 'Gi1/7'], '25', True, False, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/6', 'switchport mode trunk', 'rep segment 25', 'rep fastmode', 'shut', 'no shut', 'switchport trunk allowed vlan True', 'vlan True'],)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (['interface Gi1/7', 'switchport mode trunk', 'rep segment 25', 'rep fastmode', 'shut', 'no shut', 'switchport trunk allowed vlan True', 'vlan True'],)
        )
