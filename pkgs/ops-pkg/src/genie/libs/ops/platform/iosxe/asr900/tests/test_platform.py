# Python
import unittest

# Ats
from pyats.topology import Device

# Genie Xbu_shared
from genie.libs.ops.platform.iosxe.asr900.platform import Platform
from genie.libs.ops.platform.iosxe.asr900.tests.platform_output import PlatformOutput
from genie.libs.parser.iosxe.show_platform import ShowVersion, \
                                                        ShowRedundancy, \
                                                        ShowInventory, \
                                                        ShowPlatform
from genie.libs.parser.iosxe.show_platform import Dir
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

    def test_complete(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDir}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        f.learn()

        self.assertEqual(f.chassis, PlatformOutput.platform_all['chassis'])
        self.assertEqual(f.chassis_sn, PlatformOutput.platform_all['chassis_sn'])
        self.assertEqual(f.rtr_type, PlatformOutput.platform_all['rtr_type'])
        self.assertEqual(f.os, PlatformOutput.platform_all['os'])
        self.assertEqual(f.version, PlatformOutput.platform_all['version'])
        self.assertEqual(f.image, PlatformOutput.platform_all['image'])
        self.assertEqual(f.config_register, PlatformOutput.platform_all['config_register'])
        self.assertEqual(f.main_mem, PlatformOutput.platform_all['main_mem'])
        self.assertEqual(f.dir, PlatformOutput.platform_all['dir'])
        self.assertEqual(f.redundancy_mode, PlatformOutput.platform_all['redundancy_mode'])
        self.assertEqual(f.switchover_reason, PlatformOutput.platform_all['switchover_reason'])
        self.assertEqual(f.redundancy_communication, PlatformOutput.platform_all['redundancy_communication'])

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all['slot'])

    def test_missing_attributes_(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDir}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        f.learn()

        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['6'])

    def test_ignored(self):

        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDir}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        g.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        g.maker.outputs[Dir] = \
            {'':PlatformOutput.showDir}
        g.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        g.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        g.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        g.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        g.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff, sorted_result)

    def test_empty_parser_output(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        # loading empty output
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDirEmpty}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_empty_dir['slot'])

    def test_selective_attribute(self):

        f = Platform(device=self.device, attributes=['main_mem'])

        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.showDir}
        f.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancy}
        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowPlatform] = \
            {'':PlatformOutput.showPlatform}
        f.maker.outputs[ShowIssuStateDetail] = \
            {'':PlatformOutput.ShowIssuStateDetail}
        f.maker.outputs[ShowIssuRollbackTimer] = \
            {'':PlatformOutput.ShowIssuRollbackTimer}

        f.learn()

        self.assertIn('896500', f.main_mem)
        self.assertNotIn('111111', f.main_mem)


if __name__ == '__main__':
    unittest.main()
