# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

# Genie Xbu_shared
from genie.libs.ops.platform.nxos.platform import Platform
from genie.libs.ops.platform.nxos.tests.mando4_platform_output import PlatformOutput
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
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_sample(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {'': PlatformOutput.showInventory}
        f.maker.outputs[ShowModule] = \
            {'': PlatformOutput.showModule}
        f.maker.outputs[ShowVdcDetail] = \
            {'': PlatformOutput.showVdcDetail}
        f.maker.outputs[ShowVdcMembershipStatus] = \
            {'': PlatformOutput.showVdcMembershipStatus}
        f.maker.outputs[Dir] = \
            {'': PlatformOutput.directory}
        f.maker.outputs[ShowBoot] = \
            {'': PlatformOutput.showBoot}
        f.maker.outputs[ShowVersion] = \
            {'': PlatformOutput.showVersion}
        f.maker.outputs[ShowInstallActive] = \
            {'': PlatformOutput.showInstallActive}
        f.maker.outputs[ShowRedundancyStatus] = \
            {'': PlatformOutput.showRedundancyStatus}

        f.learn()
        self.assertEqual(f.slot, PlatformOutput.slot)


if __name__ == '__main__':
    unittest.main()
