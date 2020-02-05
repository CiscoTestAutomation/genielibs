# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

# Genie Xbu_shared
from genie.libs.ops.platform.nxos.platform import Platform
from genie.libs.ops.platform.nxos.tests.platform_output import PlatformOutput
from genie.libs.parser.nxos.show_platform import ShowVersion, \
                                                 ShowInventory, \
                                                 ShowInstallActive, \
                                                 ShowSystemRedundancyStatus, \
                                                 ShowRedundancyStatus, \
                                                 ShowBoot, \
                                                 ShowModule, \
                                                 Dir, \
                                                 ShowVdcDetail, \
                                                 ShowVdcCurrent, \
                                                 ShowVdcMembershipStatus


class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_sample(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowModule] = \
            {'':PlatformOutput.showModule}
        f.maker.outputs[ShowVdcDetail] = \
            {'':PlatformOutput.showVdcDetail}
        f.maker.outputs[ShowVdcMembershipStatus] = \
            {'':PlatformOutput.showVdcMembershipStatus}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.directory}
        f.maker.outputs[ShowBoot] = \
            {'':PlatformOutput.showBoot}
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[ShowInstallActive] = \
            {'':PlatformOutput.showInstallActive}
        f.maker.outputs[ShowRedundancyStatus] = \
            {'':PlatformOutput.showRedundancyStatus}

        f.learn()

        self.assertEqual(f.chassis, 'Nexus7000 C7009 (9 Slot) Chassis')
        self.assertEqual(f.chassis_sn, 'JAF1704ARQG')
        self.assertEqual(f.dir, 'bootflash:')
        self.assertEqual(f.disk_free_space, '1674481664')
        self.assertEqual(f.disk_total_space, '1782931456')
        self.assertEqual(f.disk_used_space, '108449792')
        self.assertEqual(f.image, 'slot0:///n7000-s2-dk10.34.1.0.129.gbin')
        self.assertEqual(f.installed_packages, 'n7700-s2-dk10.1.2.0.D1.1.CSCuo7721.bin')
        self.assertEqual(f.kickstart_image, 'slot0:///n7000-s2-kickstart.10.81.0.129.gbin')
        self.assertEqual(f.kickstart_version, 'version 8.1(1) [build 8.1(0.129)] [gdb]')
        self.assertEqual(f.main_mem, '32938744')
        self.assertEqual(f.os, 'NX-OS')
        self.assertEqual(f.rtr_type, 'Nexus7000 C7009')
        self.assertEqual(f.slot, PlatformOutput.slot)
        self.assertEqual(f.version, 'version 8.1(1) [build 8.1(0.129)] [gdb]')
        self.assertEqual(f.virtual_device, PlatformOutput.virtual_device)
        self.assertEqual(f.rp_uptime, PlatformOutput.platform_all['rp_uptime'])

    def test_missing_attributes(self):
        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowModule] = \
            {'':PlatformOutput.showModule}
        f.maker.outputs[ShowVdcDetail] = \
            {'':PlatformOutput.showVdcDetail}
        f.maker.outputs[ShowVdcMembershipStatus] = \
            {'':PlatformOutput.showVdcMembershipStatus}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.directory}
        f.maker.outputs[ShowBoot] = \
            {'':PlatformOutput.showBoot}
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[ShowInstallActive] = \
            {'':PlatformOutput.showInstallActive}
        f.maker.outputs[ShowRedundancyStatus] = \
            {'':PlatformOutput.showRedundancyStatus}

        f.learn()

        with self.assertRaises(AttributeError):
            platform_type=(f.module)

    def test_ignored(self):

        f = Platform(device=self.device)
        g = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowModule] = \
            {'':PlatformOutput.showModule}
        f.maker.outputs[ShowVdcDetail] = \
            {'':PlatformOutput.showVdcDetail}
        f.maker.outputs[ShowVdcMembershipStatus] = \
            {'':PlatformOutput.showVdcMembershipStatus}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.directory}
        f.maker.outputs[ShowBoot] = \
            {'':PlatformOutput.showBoot}
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[ShowInstallActive] = \
            {'':PlatformOutput.showInstallActive}
        f.maker.outputs[ShowRedundancyStatus] = \
            {'':PlatformOutput.showRedundancyStatus}

        g.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        g.maker.outputs[ShowModule] = \
            {'':PlatformOutput.showModule}
        g.maker.outputs[ShowVdcDetail] = \
            {'':PlatformOutput.showVdcDetail}
        g.maker.outputs[ShowVdcMembershipStatus] = \
            {'':PlatformOutput.showVdcMembershipStatus}
        g.maker.outputs[Dir] = \
            {'':PlatformOutput.directory}
        g.maker.outputs[ShowBoot] = \
            {'':PlatformOutput.showBoot}
        g.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        g.maker.outputs[ShowInstallActive] = \
            {'':PlatformOutput.showInstallActive}
        g.maker.outputs[ShowRedundancyStatus] = \
            {'':PlatformOutput.showRedundancyStatus}

        f.learn()
        g.learn()

        f.diff_ignore.append('[chassis_sn][JAF1704ARQG]')

        self.assertNotEqual(f.__dict__['diff_ignore'],g.__dict__['diff_ignore'])

    def test_selective_attribute(self):

        f = Platform(device=self.device, attributes = ['[os]'])

        f.maker.outputs[ShowInventory] = \
            {'':PlatformOutput.showInventory}
        f.maker.outputs[ShowModule] = \
            {'':PlatformOutput.showModule}
        f.maker.outputs[ShowVdcDetail] = \
            {'':PlatformOutput.showVdcDetail}
        f.maker.outputs[ShowVdcMembershipStatus] = \
            {'':PlatformOutput.showVdcMembershipStatus}
        f.maker.outputs[Dir] = \
            {'':PlatformOutput.directory}
        f.maker.outputs[ShowBoot] = \
            {'':PlatformOutput.showBoot}
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        f.maker.outputs[ShowInstallActive] = \
            {'':PlatformOutput.showInstallActive}
        f.maker.outputs[ShowRedundancyStatus] = \
            {'':PlatformOutput.showRedundancyStatus}

        f.learn()

        self.assertIn('NX-OS', f.os)
        self.assertNotIn('IOSXE', f.os)

if __name__ == '__main__':
    unittest.main()
