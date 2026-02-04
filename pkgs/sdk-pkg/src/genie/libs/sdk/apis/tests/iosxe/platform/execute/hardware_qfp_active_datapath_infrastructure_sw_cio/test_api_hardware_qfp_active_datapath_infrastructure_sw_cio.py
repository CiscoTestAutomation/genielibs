from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import hardware_qfp_active_datapath_infrastructure_sw_cio
from unittest.mock import Mock


class TestHardwareQfpActiveDatapathInfrastructureSwCio(TestCase):

    def test_hardware_qfp_active_datapath_infrastructure_sw_cio(self):
        self.device = Mock()
        results_map = {
            'show platform hardware qfp active datapath infrastructure sw-cio': 
            '''Credits Usage:

                ID      Port  Wght  Global WRKR0  WRKR1  WRKR2  WRKR3  WRKR4  Total
                 1      rcl0     4:   1452     0      0      0      0     84   1536
                 1      rcl0     8:   1472     0      0      0      0     64   1536
                 2       ipc     1:      0     0      0      0      0      0      0
                 3        lo     1:    458     0      0      0      0     54    512
                 4      eth0     1:   1952     0      0      0      0     96   2048
                 5      eth2     1:   1952     0      0      0      0     96   2048
                 6      eth1     1:   1952     0      0      0      0     96   2048
              
              Core Utilization over preceding 138432.8753 seconds
              ---------------------------------------------------
                    ID:       0       1       2       3       4 
                  % PP:    0.51    0.09    0.09    0.00    0.00 
                  % RX:    0.00    0.00    0.00    0.00    0.80 
                  % TM:    0.00    0.00    0.00    0.87    0.00 
                % COFF:    0.00    0.00    0.00    0.00    0.00 
                % IDLE:   99.49   99.91   99.91   99.13   99.20''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = hardware_qfp_active_datapath_infrastructure_sw_cio(self.device)
        self.assertIn(
            'show platform hardware qfp active datapath infrastructure sw-cio',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
