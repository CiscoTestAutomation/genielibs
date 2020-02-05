# Python
import unittest

# Ats
from pyats.topology import Device

# Genie Xbu_shared
from genie.libs.ops.platform.iosxe.c9500.platform import Platform
from genie.libs.ops.platform.iosxe.c9500.tests.platform_output import PlatformOutput
from genie.libs.parser.iosxe.c9500.show_platform import ShowVersion, \
                                                        ShowRedundancy, \
                                                        ShowInventory, \
                                                        ShowPlatform
from genie.libs.parser.iosxe.show_platform import Dir
from genie.libs.parser.iosxe.c9500.show_issu import ShowIssuStateDetail,\
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

    def test_complete_c9500(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC9500}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        f.learn()

        self.assertEqual(f.chassis, PlatformOutput.platform_all_C9500['chassis'])
        self.assertEqual(f.chassis_sn, PlatformOutput.platform_all_C9500['chassis_sn'])
        self.assertEqual(f.rtr_type, PlatformOutput.platform_all_C9500['rtr_type'])
        self.assertEqual(f.os, PlatformOutput.platform_all_C9500['os'])
        self.assertEqual(f.version, PlatformOutput.platform_all_C9500['version'])
        self.assertEqual(f.image, PlatformOutput.platform_all_C9500['image'])
        self.assertEqual(f.config_register, PlatformOutput.platform_all_C9500['config_register'])
        self.assertEqual(f.main_mem, PlatformOutput.platform_all_C9500['main_mem'])
        self.assertEqual(f.dir, PlatformOutput.platform_all_C9500['dir'])
        self.assertEqual(f.redundancy_mode, PlatformOutput.platform_all_C9500['redundancy_mode'])
        self.assertEqual(f.switchover_reason, PlatformOutput.platform_all_C9500['switchover_reason'])
        self.assertEqual(f.redundancy_communication, PlatformOutput.platform_all_C9500['redundancy_communication'])

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_C9500['slot'])

    def test_missing_attributes_c9500(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC9500}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        f.learn()
        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['6'])

    def test_ignored_c9500(self):

        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC9500}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        g.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        g.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC9500}
        g.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        g.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        g.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        g.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        g.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff, sorted_result)

    def test_empty_parser_output_c9500(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        # loading empty output
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirEmptyC9500}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_empty_dir_C9500['slot'])

    def test_selective_attribute_c9500(self):

        f = Platform(device=self.device, attributes=['main_mem'])

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersionC9500}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirC9500}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyC9500}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventoryC9500}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatformC9500}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetailC9500}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimerC9500}

        f.learn()

        self.assertIn('1863083', f.main_mem)
        self.assertNotIn('111111', f.main_mem)


if __name__ == '__main__':
    unittest.main()
