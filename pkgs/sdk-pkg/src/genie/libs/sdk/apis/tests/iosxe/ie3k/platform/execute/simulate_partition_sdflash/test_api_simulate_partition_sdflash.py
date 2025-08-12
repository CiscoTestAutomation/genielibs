from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import simulate_partition_sdflash
from unittest.mock import Mock


class TestSimulatePartitionSdflash(TestCase):

    def test_simulate_partition_sdflash(self):
        self.device = Mock()
        results_map = {
            'partition sdflash: iox': '''Partitioning IOS:IOX(30%:70%) Default
Please make sure to back-up "sdflash:" contents
Partition operation will destroy all data in "sdflash:". Continue?[confirm]
IOx Partition Already Exists, Not proceeding
Boot partition /mnt/usb2(vfat) 4.52Gig
IOx partition  /mnt/usb0(ext4) 10.4Gig

Partition of sdflash: complete'''
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = simulate_partition_sdflash(self.device)
        self.assertIn(
            'partition sdflash: iox',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = '''Executing: partition sdflash: iox
remove all configuration files! Continue? [confirm]
Partition of sdflash: complete'''
        self.assertEqual(result, expected_output)
