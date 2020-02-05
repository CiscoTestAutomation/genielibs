# Python
import unittest

# Ats
from pyats.topology import Device

# Genie Xbu_shared
from genie.libs.ops.platform.iosxe.platform import Platform
from genie.libs.ops.platform.iosxe.tests.platform_output import PlatformOutput
from genie.libs.parser.iosxe.show_platform import ShowVersion, \
                                                  Dir, \
                                                  ShowRedundancy, \
                                                  ShowInventory, \
                                                  ShowPlatform
from genie.libs.parser.iosxe.show_issu import ShowIssuStateDetail,\
                                              ShowIssuRollbackTimer


class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_asr1k(self):
        self.maxDiff = None
        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirAsr1k}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        f.learn()

        self.assertEqual(f.chassis, PlatformOutput.platform_all_asr1k['chassis'])
        self.assertEqual(f.chassis_sn, PlatformOutput.platform_all_asr1k['chassis_sn'])
        self.assertEqual(f.rtr_type, PlatformOutput.platform_all_asr1k['rtr_type'])
        self.assertEqual(f.os, PlatformOutput.platform_all_asr1k['os'])
        self.assertEqual(f.version, PlatformOutput.platform_all_asr1k['version'])
        self.assertEqual(f.image, PlatformOutput.platform_all_asr1k['image'])
        self.assertEqual(f.config_register, PlatformOutput.platform_all_asr1k['config_register'])
        self.assertEqual(f.main_mem, PlatformOutput.platform_all_asr1k['main_mem'])
        self.assertEqual(f.dir, PlatformOutput.platform_all_asr1k['dir'])
        self.assertEqual(f.redundancy_mode, PlatformOutput.platform_all_asr1k['redundancy_mode'])
        self.assertEqual(f.switchover_reason, PlatformOutput.platform_all_asr1k['switchover_reason'])
        self.assertEqual(f.redundancy_communication, PlatformOutput.platform_all_asr1k['redundancy_communication'])
        self.assertEqual(f.rp_uptime, PlatformOutput.platform_all_asr1k['rp_uptime'])
        self.assertEqual(f.issu_rollback_timer_reason, PlatformOutput.platform_all_asr1k['issu_rollback_timer_reason'])
        self.assertEqual(f.issu_rollback_timer_state, PlatformOutput.platform_all_asr1k['issu_rollback_timer_state'])
        self.assertEqual(f.slot, PlatformOutput.platform_all_asr1k['slot'])

    def test_missing_attributes_asr1k(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirAsr1k}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        f.learn()
        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['R2'])

    def test_ignored_asr1k(self):

        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirAsr1k}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        g.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        g.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirAsr1k}
        g.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        g.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        g.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        g.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        g.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff, sorted_result)

    def test_selective_attribute_asr1k(self):

        f = Platform(device=self.device, attributes=['slot[(.*)][(.*)][state]'])

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirAsr1k}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        f.learn()

        self.assertIn('ok, active', f.slot['rp']['R0']['state'])
        self.assertNotIn('ok, active',f.slot['rp']['R1']['state'])

    def test_empty_parser_output_asr1k(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionAsr1k}
        # loading empty output
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirEmptyAsr1k}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyAsr1k}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryAsr1k}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformAsr1k}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailAsr1k}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerAsr1k}

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_empty_dir_asr1k['slot'])

    def test_complete_c3850(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC3850}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        f.learn()

        self.assertEqual(f.chassis, PlatformOutput.platform_all_C3850['chassis'])
        self.assertEqual(f.chassis_sn, PlatformOutput.platform_all_C3850['chassis_sn'])
        self.assertEqual(f.rtr_type, PlatformOutput.platform_all_C3850['rtr_type'])
        self.assertEqual(f.os, PlatformOutput.platform_all_C3850['os'])
        self.assertEqual(f.version, PlatformOutput.platform_all_C3850['version'])
        self.assertEqual(f.image, PlatformOutput.platform_all_C3850['image'])
        self.assertEqual(f.config_register, PlatformOutput.platform_all_C3850['config_register'])
        self.assertEqual(f.main_mem, PlatformOutput.platform_all_C3850['main_mem'])
        self.assertEqual(f.dir, PlatformOutput.platform_all_C3850['dir'])
        self.assertEqual(f.redundancy_mode, PlatformOutput.platform_all_C3850['redundancy_mode'])
        self.assertEqual(f.switchover_reason, PlatformOutput.platform_all_C3850['switchover_reason'])
        self.assertEqual(f.redundancy_communication, PlatformOutput.platform_all_C3850['redundancy_communication'])
        self.assertEqual(f.swstack, PlatformOutput.platform_all_C3850['swstack'])

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_C3850['slot'])

    def test_missing_attributes_c3850(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC3850}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        f.learn()
        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['6'])

    def test_ignored_c3850(self):

        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC3850}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        g.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        g.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC3850}
        g.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        g.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        g.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        g.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        g.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff, sorted_result)

    def test_selective_attribute_c3850(self):

        f = Platform(device=self.device, attributes = ['slot[(.*)][(.*)][swstack_role]'])

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC3850}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        f.learn()

        self.assertIn('Active', f.slot['rp']['1']['swstack_role'])
        self.assertNotIn('Standby', f.slot['rp']['1']['swstack_role'])

    def test_empty_parser_output_c3850(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC3850}
        # loading empty output
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirEmptyC3850}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC3850}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC3850}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC3850}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC3850}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC3850}

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_empty_dir_C3850['slot'])


if __name__ == '__main__':
    unittest.main()
