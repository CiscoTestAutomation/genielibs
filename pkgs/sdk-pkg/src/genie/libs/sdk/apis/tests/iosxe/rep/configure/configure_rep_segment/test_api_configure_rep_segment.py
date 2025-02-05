from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_rep_segment
from unittest.mock import Mock


class TestConfigureRepSegment(TestCase):

    def test_configure_rep_segment(self):
        self.device = Mock()
        result = configure_rep_segment(self.device, ['GigabitEthernet1/0/1'], 1, 10, True, False, True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'switchport mode trunk', 'rep segment 1 edge', 'shut', 'no shut', 'switchport trunk allowed vlan 10', 'vlan 10'],)
        )
