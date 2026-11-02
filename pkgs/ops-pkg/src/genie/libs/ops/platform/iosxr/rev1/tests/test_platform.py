# Python
import copy
import unittest
from unittest.mock import Mock, patch

# ATS
from pyats.topology import Device

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.ops.platform.iosxr.rev1 import platform as platform_module
from genie.libs.ops.platform.iosxr.rev1.platform import Platform
from genie.libs.ops.platform.iosxr.tests.platform_output import \
    PlatformOutput as CommonOutput
from genie.libs.ops.platform.iosxr.rev1.tests.platform_output import \
    PlatformOutput

# Parser
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowSdrDetail, \
    ShowPlatform, ShowPlatformVm, \
    ShowInstallActiveSummary, ShowInventory, \
    ShowRedundancySummary, AdminShowDiagChassis, \
    ShowRedundancy, Dir
from genie.libs.parser.iosxr.rv1.show_platform import ShowDiagDetails


class test_platform(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxr')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os"]
        self.device.mapping = {'cli': 'cli'}
        mock_connection = Mock()
        mock_connection.device = self.device
        self.device.connectionmgr.connections['cli'] = mock_connection

    @staticmethod
    def _parse(output):
        def parse(**kwargs):
            if output is None:
                raise SchemaEmptyParserError(data={})
            return output
        return parse

    def _learn(self, admin_diag_chassis=None, show_inventory=None,
               show_diag_details=None):
        '''Learn Platform with the chassis serial number commands parsed
        live, so leaves are applied in the same order as on a device.'''
        p = Platform(device=self.device)
        p.maker.outputs[ShowVersion] = {'': CommonOutput.showVersionOutput}
        p.maker.outputs[ShowSdrDetail] = {'': CommonOutput.showSdrDetailOutput}
        p.maker.outputs[ShowPlatform] = {'': CommonOutput.showPlatformOutput}
        p.maker.outputs[ShowPlatformVm] = \
            {'': CommonOutput.showPlatformVmOutput}
        p.maker.outputs[ShowInstallActiveSummary] = \
            {'': CommonOutput.showInstallActiveSummaryOutput}
        p.maker.outputs[ShowRedundancySummary] = \
            {'': CommonOutput.showRedundancySummaryOutput}
        p.maker.outputs[ShowRedundancy] = \
            {'': CommonOutput.showRedundancyOutput}
        p.maker.outputs[Dir] = {'': CommonOutput.dirOutput}

        with patch.object(AdminShowDiagChassis, 'parse',
                          side_effect=self._parse(admin_diag_chassis)), \
             patch.object(ShowInventory, 'parse',
                          side_effect=self._parse(show_inventory)), \
             patch.object(ShowDiagDetails, 'parse',
                          side_effect=self._parse(show_diag_details)):
            p.learn()
        return p

    def test_chassis_sn_ncs5501(self):
        p = self._learn(
            admin_diag_chassis=PlatformOutput.ncs5501AdminShowDiagChassisOutput,
            show_inventory=PlatformOutput.ncs5501ShowInventoryOutput,
            show_diag_details=PlatformOutput.ncs5501ShowDiagDetailsOutput)

        self.assertEqual(p.chassis_sn, 'FOC2335R0FK')

    def test_chassis_sn_8201(self):
        p = self._learn(
            show_diag_details=PlatformOutput.c8201ShowDiagDetailsOutput)

        self.assertEqual(p.chassis_sn, 'FLM263401XF')

    def test_chassis_sn_8011(self):
        p = self._learn(
            show_inventory=PlatformOutput.c8011ShowInventoryOutput,
            show_diag_details=PlatformOutput.c8011ShowDiagDetailsOutput)

        self.assertEqual(p.chassis_sn, 'FDO29180127')

    def test_chassis_sn_inventory_wins_over_common_blocks(self):
        with self.assertLogs(platform_module.logger, 'WARNING') as cm:
            p = self._learn(
                show_inventory=(
                    PlatformOutput.commonBlocksOnlyShowInventoryOutput),
                show_diag_details=(
                    PlatformOutput.commonBlocksOnlyShowDiagDetailsOutput))

        self.assertEqual(p.chassis_sn, 'FOC2335R0FK')
        self.assertEqual(len(cm.output), 1)
        self.assertIn('FOC2335R0FK', cm.output[0])
        self.assertIn('FOC23332ACR', cm.output[0])

    def test_chassis_sn_ncs5501_inventory_missing(self):
        p = self._learn(
            admin_diag_chassis=PlatformOutput.ncs5501AdminShowDiagChassisOutput,
            show_inventory=None,
            show_diag_details=PlatformOutput.ncs5501ShowDiagDetailsOutput)

        self.assertEqual(p.chassis_sn, 'FOC2335R0FK')

    def test_chassis_sn_inventory_na_falls_back_to_diag(self):
        inventory = copy.deepcopy(PlatformOutput.ncs5501ShowInventoryOutput)
        inventory['module_name']['Rack 0']['sn'] = 'N/A'
        admin_diag = copy.deepcopy(
            PlatformOutput.ncs5501AdminShowDiagChassisOutput)
        del admin_diag['top_assembly_block']

        p = self._learn(admin_diag_chassis=admin_diag,
                        show_inventory=inventory)

        self.assertEqual(p.chassis_sn, 'FOC23332ACR')

    def test_chassis_sn_no_warning_when_inventory_matches_diag(self):
        with patch.object(platform_module.logger, 'warning') as warning:
            p = self._learn(
                admin_diag_chassis=(
                    PlatformOutput.ncs5501AdminShowDiagChassisOutput),
                show_inventory=PlatformOutput.ncs5501ShowInventoryOutput,
                show_diag_details=PlatformOutput.ncs5501ShowDiagDetailsOutput)

        self.assertEqual(p.chassis_sn, 'FOC2335R0FK')
        warning.assert_not_called()


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
