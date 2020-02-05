# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie Xbu_shared
from genie.libs.ops.platform.ios.cat6k.platform import Platform
from genie.libs.ops.platform.ios.cat6k.tests.platform_output import PlatformOutput
from genie.libs.parser.ios.cat6k.show_platform import ShowVersion, \
                                                      Dir, \
                                                      ShowRedundancy, \
                                                      ShowInventory, \
                                                      ShowModule

def mapper(f):
    outputs_dict = {
        ShowVersion: PlatformOutput.showVersionCat6k,
        Dir: PlatformOutput.dirCat6k,
        ShowRedundancy: PlatformOutput.showRedundancyCat6k,
        ShowInventory: PlatformOutput.showInventoryCat6k,
        ShowModule: PlatformOutput.showModuleCat6k
    }
    for k, v in outputs_dict.items():
        f.maker.outputs[k] = {'': v}

    return f


class TestPlatformAll(unittest.TestCase):
    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.custom['abstraction'] = {'order': ['os']}
        self.device.platform = 'cat6k'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_cat6k(self):
        f = Platform(device=self.device)
        f = mapper(f)
        f.learn()

        self.assertEqual(f.chassis, PlatformOutput.platform_all_cat6k['chassis'])
        self.assertEqual(f.os, PlatformOutput.platform_all_cat6k['os'])
        self.assertEqual(f.version, PlatformOutput.platform_all_cat6k['version'])
        self.assertEqual(f.image, PlatformOutput.platform_all_cat6k['image'])
        self.assertEqual(f.rtr_type, PlatformOutput.platform_all_cat6k['rtr_type'])
        self.assertEqual(f.config_register, PlatformOutput.platform_all_cat6k['config_register'])
        self.assertEqual(f.main_mem, PlatformOutput.platform_all_cat6k['main_mem'])
        self.assertEqual(f.dir, PlatformOutput.platform_all_cat6k['dir'])
        self.assertEqual(f.redundancy_mode, PlatformOutput.platform_all_cat6k['redundancy_mode'])
        self.assertEqual(f.switchover_reason, PlatformOutput.platform_all_cat6k['switchover_reason'])
        self.assertEqual(f.redundancy_communication, PlatformOutput.platform_all_cat6k['redundancy_communication'])

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_cat6k['slot'])

    def test_missing_attributes_cat6k(self):
        f = Platform(device=self.device)
        f = mapper(f)
        f.learn()
        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['6'])

    def test_ignored_cat6k(self):
        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f = mapper(f)
        g = mapper(g)

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f, g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff, sorted_result)

    def test_empty_parser_output_cat6k(self):
        f = Platform(device=self.device)

        f.maker.outputs[ShowVersion] = \
            {'': PlatformOutput.showVersionCat6k}
        # loading empty output
        f.maker.outputs[Dir] = \
            {'': PlatformOutput.dirEmptyCat6k}
        f.maker.outputs[ShowRedundancy] = \
            {'': PlatformOutput.showRedundancyCat6k}
        f.maker.outputs[ShowInventory] = \
            {'': PlatformOutput.showInventoryCat6k}
        f.maker.outputs[ShowModule] = \
            {'': PlatformOutput.showModuleCat6k}

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.slot, PlatformOutput.platform_all_cat6k['slot'])

    def test_selective_attribute_cat6k(self):
        f = Platform(device=self.device, attributes=['main_mem'])
        f = mapper(f)
        f.learn()

        self.assertIn('983008', f.main_mem)
        self.assertNotIn('111111', f.main_mem)


if __name__ == '__main__':
    unittest.main()