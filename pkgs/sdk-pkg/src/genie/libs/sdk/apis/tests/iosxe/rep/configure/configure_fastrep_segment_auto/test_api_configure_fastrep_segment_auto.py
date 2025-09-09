from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_fastrep_segment_auto
from unittest.mock import Mock


class TestConfigureFastrepSegmentAuto(TestCase):

    def test_configure_fastrep_segment_auto(self):
        self.device = Mock()
        result = configure_fastrep_segment_auto(self.device, ['Gi1/6', 'Gi1/7'], '25', True, False, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/6', 'switchport mode trunk', 'rep segment auto', 'rep fastmode', 'shut', 'no shut'],)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (['interface Gi1/7', 'switchport mode trunk', 'rep segment auto', 'rep fastmode', 'shut', 'no shut'],)
        )
