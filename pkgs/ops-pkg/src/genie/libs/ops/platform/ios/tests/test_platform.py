# Python
import unittest
from unittest.mock import Mock
# Ats
from pyats.topology import Device

# Genie Xbu_shared
from genie.libs.ops.platform.ios.platform import Platform
from genie.libs.ops.platform.ios.tests.platform_output import PlatformOutput

outputs = {
    'show version': PlatformOutput.show_version,
    'dir': PlatformOutput.dir_ios,
    'show inventory': PlatformOutput.show_inventory,
}


def mapper(key):
    return outputs[key]


class TestPlatformAll(unittest.TestCase):

    def setUp(self):
        self.device = Device(name="aDevice")
        self.device.os = "ios"
        self.device.mapping = {}
        self.device.mapping["cli"] = "cli"
        self.device.custom['abstraction'] = {'order': ['os']}
        self.device.platform = 'cat6k'
        self.device.connectionmgr.connections["cli"] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        platform = Platform(device=self.device)

        # Learn the feature
        platform.learn()

        self.assertEqual(platform.main_mem, PlatformOutput.platform_all['main_mem'])
        self.assertEqual(platform.rtr_type, PlatformOutput.platform_all['rtr_type'])
        self.assertEqual(platform.chassis, PlatformOutput.platform_all['chassis'])
        self.assertEqual(platform.chassis_sn, PlatformOutput.platform_all['chassis_sn'])
        self.assertEqual(platform.os, PlatformOutput.platform_all['os'])
        self.assertEqual(platform.version, PlatformOutput.platform_all['version'])
        self.assertEqual(platform.image, PlatformOutput.platform_all['image'])
        self.assertEqual(platform.config_register, PlatformOutput.platform_all['config_register'])
        self.assertEqual(platform.dir, PlatformOutput.platform_all['dir'])
        self.assertEqual(platform.slot, PlatformOutput.platform_all['slot'])

    def test_missing_attributes(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        f = Platform(device=self.device)

        f.maker.outputs['show version'] = \
            {'': PlatformOutput.show_version}
        f.maker.outputs['dir'] = \
            {'': PlatformOutput.dir_ios}
        f.maker.outputs['show inventory'] = \
            {'': PlatformOutput.show_inventory}

        f.learn()
        with self.assertRaises(KeyError):
            # slot 'R2' doesn't exist
            platform_slot_number = (f.slot['slot']['R2'])

    def test_selective_attribute_asr1k(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        f = Platform(device=self.device, attributes=['[os]'])

        f.maker.outputs['show version'] = \
            {'': PlatformOutput.show_version}
        f.maker.outputs['dir'] = \
            {'': PlatformOutput.dir_ios}
        f.maker.outputs['show inventory'] = \
            {'': PlatformOutput.show_inventory}

        f.learn()

        self.assertIn('ios', f.os)
        self.assertNotIn('iosv', f.os)

    def test_empty_parser_output(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        f = Platform(device=self.device)

        f.maker.outputs['show version'] = \
            {'': PlatformOutput.show_version}
        f.maker.outputs['dir'] = \
            {'': PlatformOutput.dir_ios}
        f.maker.outputs['show inventory'] = \
            {'': PlatformOutput.show_inventory}

        f.learn()

        self.assertEqual(f.slot, PlatformOutput.platform_all['slot'])