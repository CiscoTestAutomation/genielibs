# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.ops.base import Base
from genie.ops.base.maker import Maker
from genie.libs.ops.platform.iosxr.platform import Platform
from genie.libs.ops.platform.iosxr.tests.platform_output import PlatformOutput

# Parser
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowSdrDetail,\
                                ShowPlatform, ShowPlatformVm,\
                                ShowInstallActiveSummary, ShowInventory,\
                                ShowRedundancySummary, AdminShowDiagChassis,\
                                ShowRedundancy, Dir


class test_platform(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_all_attributes(self):
        self.maxDiff = None
        p = Platform(device=self.device)
        # Get 'show version' output
        p.maker.outputs[ShowVersion] = {'':PlatformOutput.showVersionOutput}
        # Get 'show sdr detail' output
        p.maker.outputs[ShowSdrDetail] = {'':PlatformOutput.showSdrDetailOutput}
        # Get 'show platform' output
        p.maker.outputs[ShowPlatform] = {'':PlatformOutput.showPlatformOutput}
        # Get 'show platform vm' output
        p.maker.outputs[ShowPlatformVm] = {'':PlatformOutput.showPlatformVmOutput}
        # Get 'show install active summar' output
        p.maker.outputs[ShowInstallActiveSummary] = \
            {'':PlatformOutput.showInstallActiveSummaryOutput}
        # Get 'show inventory' output
        p.maker.outputs[ShowInventory] = {'':PlatformOutput.showInventoryOutput}
        # Get 'show redundancy summary' output
        p.maker.outputs[ShowRedundancySummary] = \
            {'':PlatformOutput.showRedundancySummaryOutput}
        # Get 'show redundancy' output
        p.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyOutput}
        # Get 'admin show diag chassis' output
        p.maker.outputs[AdminShowDiagChassis] = \
            {'':PlatformOutput.adminShowDiagChassisOutput}
        # Get 'dir' output
        p.maker.outputs[Dir] = {'':PlatformOutput.dirOutput}
        # Learn the feature
        p.learn()

        # Check all match
        self.assertEqual(p.chassis, 'ASR 9006 4 Line Card Slot Chassis with V2 AC PEM')
        self.assertEqual(p.chassis_sn, 'FOX1810G8LR')
        self.assertEqual(p.config_register, '0x1922')
        dir_value = {
            'dir_name': 'disk0a:/usr',
            'total_bytes': '2562719744 bytes',
            'total_free_bytes': '1918621184 bytes'}
        self.assertEqual(p.dir, dir_value)
        self.assertEqual(p.image, 'disk0:asr9k-os-mbi-6.1.4.10I/0x100305/mbiasr9k-rsp3.vm')
        packages = ['disk0:asr9k-mini-px-6.1.21.15I',
                    'disk0:asr9k-mpls-px-6.1.21.15I',
                    'disk0:asr9k-mcast-px-6.1.21.15I',
                    'disk0:asr9k-mgbl-px-6.1.21.15I']
        self.assertEqual(p.installed_packages, packages)
        self.assertEqual(p.main_mem, '6291456K')
        self.assertEqual(p.os, 'IOSXR')
        self.assertEqual(p.rtr_type, 'ASR9K')
        self.assertEqual(p.sdr_owner, 'Owner')
        self.assertEqual(p.version, '6.1.4.10I')
        self.assertEqual(p.rp_uptime, 480)
        slots = {
            'lc': {
                '0/0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-MOD80-SE',
                    'state': 'IOS XR RUN',
                    'subslot': {
                        '0': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MPA-20X1GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '1': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MQA-20X2GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '2': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MRA-20X3GE',
                            'redundancy_state': 'None',
                            'state': 'OK'}}}},
            'rp': {
                '0/RSP0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Active',
                    'state': 'IOS XR RUN'},
                '0/RSP1': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Standby',
                    'state': 'IOS XR RUN'},
                'rp_config_register': '0x1922'}}
        self.assertEqual(p.slot, slots)
        virtual_device_dict = {
            0: {
                'membership': {
                    '0/0/CPU0': {
                        'vd_ms_partner_name': 'NONE',
                        'vd_ms_red_state': 'Not-known',
                        'vd_ms_status': 'IOS '
                                        'XR '
                                        'RUN',
                        'vd_ms_type': 'LC'},
                    '0/RSP0/CPU0': {
                        'vd_ms_partner_name': '0/RSP1/CPU0',
                        'vd_ms_red_state': 'Primary',
                        'vd_ms_status': 'IOS '
                                       'XR '
                                       'RUN',
                       'vd_ms_type': 'RP'},
                    '0/RSP1/CPU0': {
                        'vd_ms_partner_name': '0/RSP0/CPU0',
                        'vd_ms_red_state': 'Backup',
                        'vd_ms_status': 'IOS '
                                       'XR '
                                       'RUN',
                        'vd_ms_type': 'RP'}},
                'vd_dSDRsc_nod': '0/RSP0/CPU0',
                'vd_dSDRsc_partner_node': '0/RSP1/CPU0',
                'vd_mac_addr': 'a80c.0d5f.ab17',
                'vd_name': 'Owner',
                'vd_primary_node1': '0/RSP0/CPU0',
                'vd_primary_node2': '0/RSP1/CPU0'}}
        self.assertEqual(p.virtual_device, virtual_device_dict)


    def test_missing_attributes(self):
        self.maxDiff = None
        p = Platform(device=self.device)
        # Get 'show version' output
        p.maker.outputs[ShowVersion] = {'':PlatformOutput.showVersionOutput}
        # Get 'show sdr detail' output
        p.maker.outputs[ShowSdrDetail] = {'':PlatformOutput.showSdrDetailOutput}
        # Get 'show platform' output
        p.maker.outputs[ShowPlatform] = {'':PlatformOutput.showPlatformOutput}
        # Get 'show platform vm' output
        p.maker.outputs[ShowPlatformVm] = {'':PlatformOutput.showPlatformVmOutput}
        # Get 'show install active summar' output
        p.maker.outputs[ShowInstallActiveSummary] = \
            {'':PlatformOutput.showInstallActiveSummaryOutput}
        # Get 'show inventory' output
        p.maker.outputs[ShowInventory] = {'':PlatformOutput.showInventoryOutput}
        # Get 'show redundancy summary' output
        p.maker.outputs[ShowRedundancySummary] = \
            {'':PlatformOutput.showRedundancySummaryOutput}
        # Get 'show redundancy' output
        p.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyOutput}
        # Get 'admin show diag chassis' output
        p.maker.outputs[AdminShowDiagChassis] = \
            {'':PlatformOutput.adminShowDiagChassisOutput}
        # Get 'dir' output
        p.maker.outputs[Dir] = {'':PlatformOutput.dirOutput}
        # Learn the feature
        p.learn()

        # Check attribute not found
        with self.assertRaises(AttributeError):
            platform_type=(p.module)


    def test_selective_attribute(self):
        self.maxDiff = None
        p = Platform(device=self.device)
        # Get 'show version' output
        p.maker.outputs[ShowVersion] = {'':PlatformOutput.showVersionOutput}
        # Get 'show sdr detail' output
        p.maker.outputs[ShowSdrDetail] = {'':PlatformOutput.showSdrDetailOutput}
        # Get 'show platform' output
        p.maker.outputs[ShowPlatform] = {'':PlatformOutput.showPlatformOutput}
        # Get 'show platform vm' output
        p.maker.outputs[ShowPlatformVm] = {'':PlatformOutput.showPlatformVmOutput}
        # Get 'show install active summar' output
        p.maker.outputs[ShowInstallActiveSummary] = \
            {'':PlatformOutput.showInstallActiveSummaryOutput}
        # Get 'show inventory' output
        p.maker.outputs[ShowInventory] = {'':PlatformOutput.showInventoryOutput}
        # Get 'show redundancy summary' output
        p.maker.outputs[ShowRedundancySummary] = \
            {'':PlatformOutput.showRedundancySummaryOutput}
        # Get 'show redundancy' output
        p.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyOutput}
        # Get 'admin show diag chassis' output
        p.maker.outputs[AdminShowDiagChassis] = \
            {'':PlatformOutput.adminShowDiagChassisOutput}
        # Get 'dir' output
        p.maker.outputs[Dir] = {'':PlatformOutput.dirOutput}
        # Learn the feature
        p.learn()

        # Check selective attribute value
        self.assertIn('IOSXR', p.os)
        self.assertNotIn('IOSXE', p.os)


    def test_ignored(self):
        self.maxDiff = None
        
        p1 = Platform(device=self.device)
        # Get 'show version' output
        p1.maker.outputs[ShowVersion] = {'':PlatformOutput.showVersionOutput}
        # Get 'show sdr detail' output
        p1.maker.outputs[ShowSdrDetail] = {'':PlatformOutput.showSdrDetailOutput}
        # Get 'show platform' output
        p1.maker.outputs[ShowPlatform] = {'':PlatformOutput.showPlatformOutput}
        # Get 'show platform vm' output
        p1.maker.outputs[ShowPlatformVm] = {'':PlatformOutput.showPlatformVmOutput}
        # Get 'show install active summar' output
        p1.maker.outputs[ShowInstallActiveSummary] = \
            {'':PlatformOutput.showInstallActiveSummaryOutput}
        # Get 'show inventory' output
        p1.maker.outputs[ShowInventory] = {'':PlatformOutput.showInventoryOutput}
        # Get 'show redundancy summary' output
        p1.maker.outputs[ShowRedundancySummary] = \
            {'':PlatformOutput.showRedundancySummaryOutput}
        # Get 'show redundancy' output
        p1.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyOutput}
        # Get 'admin show diag chassis' output
        p1.maker.outputs[AdminShowDiagChassis] = \
            {'':PlatformOutput.adminShowDiagChassisOutput}
        # Get 'dir' output
        p1.maker.outputs[Dir] = {'':PlatformOutput.dirOutput}

        p2 = Platform(device=self.device)
        # Get 'show version' output
        p2.maker.outputs[ShowVersion] = {'':PlatformOutput.showVersionOutput}
        # Get 'show sdr detail' output
        p2.maker.outputs[ShowSdrDetail] = {'':PlatformOutput.showSdrDetailOutput}
        # Get 'show platform' output
        p2.maker.outputs[ShowPlatform] = {'':PlatformOutput.showPlatformOutput}
        # Get 'show platform vm' output
        p2.maker.outputs[ShowPlatformVm] = {'':PlatformOutput.showPlatformVmOutput}
        # Get 'show install active summar' output
        p2.maker.outputs[ShowInstallActiveSummary] = \
            {'':PlatformOutput.showInstallActiveSummaryOutput}
        # Get 'show inventory' output
        p2.maker.outputs[ShowInventory] = {'':PlatformOutput.showInventoryOutput}
        # Get 'show redundancy summary' output
        p2.maker.outputs[ShowRedundancySummary] = \
            {'':PlatformOutput.showRedundancySummaryOutput}
        # Get 'show redundancy' output
        p2.maker.outputs[ShowRedundancy] = \
            {'':PlatformOutput.showRedundancyOutput}
        # Get 'admin show diag chassis' output
        p2.maker.outputs[AdminShowDiagChassis] = \
            {'':PlatformOutput.adminShowDiagChassisOutput}
        # Get 'dir' output
        p2.maker.outputs[Dir] = {'':PlatformOutput.dirOutput}
        
        # Learn the feature
        p1.learn()
        p2.learn()

        p1.diff_ignore.append('[chassis_sn][JAF1704ARQG]')

        self.assertNotEqual(p1.__dict__['diff_ignore'],p2.__dict__['diff_ignore'])


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
