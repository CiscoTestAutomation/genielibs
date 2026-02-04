from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import hardware_qfp_active_datapath_utilization
from unittest.mock import Mock


class TestHardwareQfpActiveDatapathUtilization(TestCase):

    def test_hardware_qfp_active_datapath_utilization(self):
        self.device = Mock()
        results_map = {
            'show platform hardware qfp active datapath utilization': 
            '''  CPP 0: Subdev 0            5 secs        1 min        5 min       60 min
              Input:  Priority (pps)            0            0            0            0
                               (bps)            0            0            0            0
                  Non-Priority (pps)            2            3            3            3
                               (bps)          928         1328         1368         1344
                         Total (pps)            2            3            3            3
                               (bps)          928         1328         1368         1344
              Output: Priority (pps)            0            0            0            0
                               (bps)            0            0            0            0
                  Non-Priority (pps)            1            1            1            1
                               (bps)         2864         8728         8776         8728
                         Total (pps)            1            1            1            1
                               (bps)         2864         8728         8776         8728
              Processing: Load (pct)            0            0            0            0
              
              Crypto/IO
                  Crypto: Load (pct)            0            0            0            0
                      RX: Load (pct)            0            0            0            0
                      TX: Load (pct)            0            0            0            0
                          Idle (pct)           99           99           99           99''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = hardware_qfp_active_datapath_utilization(self.device)
        self.assertIn(
            'show platform hardware qfp active datapath utilization',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
