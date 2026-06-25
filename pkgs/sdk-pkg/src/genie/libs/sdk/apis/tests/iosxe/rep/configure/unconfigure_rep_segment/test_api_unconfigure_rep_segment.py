import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rep.configure import (
    unconfigure_rep_segment
)


class TestUnconfigureRepSegment(unittest.TestCase):

    def test_unconfigure_rep_segment(self):
        device = Mock()

        result = unconfigure_rep_segment(
            device,
            ['Gi1/6', 'Gi1/7'],
            '25',
            True,
            False,
            False,
            False
        )

        self.assertEqual(result, None)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Gi1/6',
              'no rep segment 25',
              'no rep fastmode',
              'no switchport mode trunk',
              'no shut',
              'shut',
              'no switchport trunk allowed vlan True',
              'no vlan True'],)
        )

        self.assertEqual(
            device.configure.mock_calls[1].args,
            (['interface Gi1/7',
              'no rep segment 25',
              'no rep fastmode',
              'no switchport mode trunk',
              'no shut',
              'shut',
              'no switchport trunk allowed vlan True',
              'no vlan True'],)
        )