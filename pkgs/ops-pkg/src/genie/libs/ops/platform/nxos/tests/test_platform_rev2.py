# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

# Genie Xbu_shared
from genie.libs.ops.platform.nxos.rev2.platform import Platform
from genie.libs.ops.platform.nxos.tests.rev2_platform_output import PlatformOutput
from genie.libs.parser.nxos.show_platform import ShowVersion, \
                                                 ShowInventory, \
                                                 ShowInstallActive, \
                                                 ShowRedundancyStatus, \
                                                 ShowBoot, \
                                                 ShowModule, \
                                                 Dir, \
                                                 ShowVdcDetail, \
                                                 ShowVdcMembershipStatus


class test_platform_rev2_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_sample(self):

        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {"{'option':'all'}": PlatformOutput.showInventory}
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
        self.assertIn('rp', f.slot, 'slot[rp] entry not found')
        self.assertIn('lc', f.slot, 'slot[lc] entry not found')

    def test_complete_output(self):
        """Test all major platform attributes are learned correctly"""
        
        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {"{'option':'all'}": PlatformOutput.showInventory}
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
        
        # Test chassis information
        self.assertEqual(f.chassis, PlatformOutput.showInventory['name']['Chassis']['pid'])
        self.assertEqual(f.chassis_sn, PlatformOutput.showInventory['name']['Chassis']['serial_number'])
        
        # Test system information
        self.assertEqual(f.rtr_type, PlatformOutput.showVersion['platform']['hardware']['model'])
        self.assertEqual(f.os, PlatformOutput.showVersion['platform']['os'])
        self.assertEqual(f.version, PlatformOutput.showVersion['platform']['software']['system_version'])
        self.assertEqual(f.image, PlatformOutput.showVersion['platform']['software']['system_image_file'])
        self.assertEqual(f.main_mem, PlatformOutput.showVersion['platform']['hardware']['memory'])
        
        # Test disk information
        self.assertEqual(f.disk_used_space, PlatformOutput.directory['disk_used_space'])
        self.assertEqual(f.disk_free_space, PlatformOutput.directory['disk_free_space'])
        self.assertEqual(f.disk_total_space, PlatformOutput.directory['disk_total_space'])
        self.assertEqual(f.dir, PlatformOutput.directory['dir'])
        
    def test_slot_structure(self):
        """Test slot structure contains all required hardware types"""
        
        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {"{'option':'all'}": PlatformOutput.showInventory}
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
        
        # Test slot contains all hardware types
        self.assertIn('rp', f.slot, 'Route Processor not found in slot')
        self.assertIn('lc', f.slot, 'Line Card not found in slot')
        self.assertIn('fan', f.slot, 'Fan modules not found in slot')
        self.assertIn('psu', f.slot, 'Power Supply not found in slot')
        self.assertIn('transceiver', f.slot, 'Transceivers not found in slot')
        
        # Test RP attributes
        self.assertIn('27', f.slot['rp'], 'RP slot 27 not found')
        rp = f.slot['rp']['27']
        self.assertIn('name', rp, 'RP name not found')
        self.assertIn('state', rp, 'RP state not found')
        self.assertIn('sn', rp, 'RP serial number not found')
        self.assertIn('rp_boot_image', rp, 'RP boot image not found')
        self.assertIn('rp_uptime', rp, 'RP uptime not found')
        
        # Test LC attributes
        self.assertIn('1', f.slot['lc'], 'LC slot 1 not found')
        lc = f.slot['lc']['1']
        self.assertIn('name', lc, 'LC name not found')
        self.assertIn('pid', lc, 'LC PID not found')
        self.assertIn('sn', lc, 'LC serial number not found')
        self.assertIn('state', lc, 'LC state not found')
        
        # Test Fan attributes
        self.assertIn('Fan 1', f.slot['fan'], 'Fan 1 not found')
        self.assertIn('Fan 2', f.slot['fan'], 'Fan 2 not found')
        self.assertIn('Fan 3', f.slot['fan'], 'Fan 3 not found')
        
        # Test PSU attributes
        self.assertIn('PSU1', f.slot['psu'], 'PSU1 not found')
        psu = f.slot['psu']['PSU1']
        self.assertIn('name', psu, 'PSU name not found')
        self.assertIn('pid', psu, 'PSU PID not found')
        self.assertIn('sn', psu, 'PSU serial number not found')

    def test_virtual_device_structure(self):
        """Test virtual device context (VDC) structure"""
        
        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {"{'option':'all'}": PlatformOutput.showInventory}
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
        
        # Test virtual device structure
        self.assertIn('virtual_device', f.__dict__, 'Virtual device not found')
        self.assertIn('1', f.virtual_device, 'VDC 1 not found')
        
        vdc = f.virtual_device['1']
        self.assertIn('vd_name', vdc, 'VDC name not found')
        self.assertIn('vd_status', vdc, 'VDC status not found')
        self.assertIn('membership', vdc, 'VDC membership not found')
        
        # Verify VDC name and status
        self.assertEqual(vdc['vd_name'], 'n9k-fanout')
        self.assertEqual(vdc['vd_status'], 'active')
        
        # Verify membership is a dictionary
        self.assertIsInstance(vdc['membership'], dict, 'VDC membership should be a dictionary')
        
        # Verify membership contains interfaces
        self.assertIn('Eth1/1', vdc['membership'], 'Interface Eth1/1 not in membership')
        
        # Verify interface attributes
        intf = vdc['membership']['Eth1/1']
        self.assertIn('status', intf, 'Interface status not found')
        self.assertIn('type', intf, 'Interface type not found')
        self.assertEqual(intf['status'], 'OK')
        self.assertEqual(intf['type'], 'Ethernet')

    def test_transceiver_structure(self):
        """Test transceiver structure and organization"""
        
        f = Platform(device=self.device)

        f.maker.outputs[ShowInventory] = \
            {"{'option':'all'}": PlatformOutput.showInventory}
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
        
        # Test transceiver structure
        self.assertIn('transceiver', f.slot, 'Transceivers not found')
        self.assertIn('1', f.slot['transceiver'], 'Module 1 transceivers not found')
        
        # Verify multiple transceivers exist
        transceivers = f.slot['transceiver']['1']
        self.assertGreater(len(transceivers), 0, 'No transceivers found')
        
        # Test specific transceiver 15
        self.assertIn('transceiver 22', transceivers, 'transceiver 22 not found')
        xcvr15 = transceivers['transceiver 22']
        self.assertIn('name', xcvr15, 'Transceiver 22 name not found')
        self.assertIn('pid', xcvr15, 'Transceiver 22 PID not found')
        self.assertIn('sn', xcvr15, 'Transceiver 22 serial number not found')
        
        # Verify transceiver 22 specific values
        self.assertEqual(xcvr15['name'], 'CISCO-FINISAR', 'Transceiver 22 name mismatch')
        self.assertEqual(xcvr15['pid'], 'QSFP-100G-AOC1M', 'Transceiver 22 PID mismatch')
        self.assertEqual(xcvr15['sn'], 'FIW222701HY-B', 'Transceiver 22 serial number mismatch')

if __name__ == '__main__':
    unittest.main()
