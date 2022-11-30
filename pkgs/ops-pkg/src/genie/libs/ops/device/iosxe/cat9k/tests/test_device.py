# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.device.iosxe.cat9k.device import Device as DeviceModel
from genie.libs.ops.device.iosxe.cat9k.tests.device_output import DeviceOutput

# Parser
from genie.libs.ops.device.device import ShowRunningConfig
from genie.libs.parser.iosxe.show_cdp import ShowCdpNeighborsDetail
from genie.libs.parser.iosxe.show_lldp import ShowLldpNeighborsDetail
from genie.libs.parser.iosxe.show_interface import ShowInterfaces
from genie.libs.parser.iosxe.show_inventory import ShowInventoryRaw
from genie.libs.parser.iosxe.show_fdb import ShowMacAddressTable
from genie.libs.parser.iosxe.show_power import ShowPowerInline
from genie.libs.parser.iosxe.show_platform import ShowBoot, ShowEnvAll, ShowVersion

outputs = {
    'show boot': DeviceOutput.ShowBoot,
    'show cdp neighbors detail': DeviceOutput.ShowCdpNeighborsDetail,
    'show env all': DeviceOutput.ShowEnvAll,
    'show interfaces': DeviceOutput.ShowInterfaces,
    'show inventory raw': DeviceOutput.ShowInventoryRaw,
    'show lldp neighbors detail': DeviceOutput.ShowLldpNeighborsDetail,
    'show mac address-table': DeviceOutput.ShowMacAddressTable,
    'show power inline': DeviceOutput.ShowPowerInline,
    'show running-config': DeviceOutput.ShowRunningConfig,
    'show version': DeviceOutput.ShowVersion
}


def mapper(key):
    return outputs[key]


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxe', type='cat9k')
        self.device.custom.setdefault("abstraction", {})["order"] = ["type", "os"]
        self.device.mapping = {'cli': 'cli'}
        mock_device = Mock()
        self.device.connectionmgr.connections['cli'] = mock_device
        mock_device.execute.side_effect = mapper

    def test_output_with_attribute(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device,
                          attributes=['info[version][(.*)]'])

        # Get outputs
        dev.maker.outputs[ShowVersion] = {
            '': DeviceOutput.ShowVersion
        }

        # learn the feature
        dev.learn()

        self.assertDictEqual(
            dev.info['version'],
            DeviceOutput.DeviceInfo['version'])

        # asserts that version is the only key in info
        self.assertEqual(
            list(dev.info.keys()),
            ['version'])

    def test_empty_output(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device)

        # Get outputs
        dev.maker.outputs[ShowBoot] = {'': {}}
        dev.maker.outputs[ShowCdpNeighborsDetail] = {'': {}}
        dev.maker.outputs[ShowEnvAll] = {'': {}}
        dev.maker.outputs[ShowInterfaces] = {'': {}}
        dev.maker.outputs[ShowInventoryRaw] = {'': {}}
        dev.maker.outputs[ShowLldpNeighborsDetail] = {'': {}}
        dev.maker.outputs[ShowMacAddressTable] = {'': {}}
        dev.maker.outputs[ShowPowerInline] = {'': {}}
        dev.maker.outputs[ShowRunningConfig] = {'': {}}
        dev.maker.outputs[ShowVersion] = {'': {}}

        dev.learn()

        # Check info was not created
        self.assertFalse(hasattr(dev, 'info'))

    def test_complete_output(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device)

        # Get outputs
        dev.maker.outputs[ShowBoot] = {
            '': DeviceOutput.ShowBoot
        }

        dev.maker.outputs[ShowCdpNeighborsDetail] = {
            '': DeviceOutput.ShowCdpNeighborsDetail}

        dev.maker.outputs[ShowInterfaces] = {
            '': DeviceOutput.ShowInterfaces}

        dev.maker.outputs[ShowInventoryRaw] = {
            '': DeviceOutput.ShowInventoryRaw}

        dev.maker.outputs[ShowLldpNeighborsDetail] = {
            '': DeviceOutput.ShowLldpNeighborsDetail}

        dev.maker.outputs[ShowVersion] = {
            '': DeviceOutput.ShowVersion}

        dev.maker.outputs[ShowEnvAll] = {
            '': DeviceOutput.ShowEnvAll}

        dev.maker.outputs[ShowMacAddressTable] = {
            '': DeviceOutput.ShowMacAddressTable}

        dev.maker.outputs[ShowPowerInline] = {
            '': DeviceOutput.ShowPowerInline}

        dev.maker.outputs[ShowRunningConfig] = {
            '': DeviceOutput.ShowRunningConfig}

        dev.learn()

        expected_keys = [
            'bootvar', 'config', 'environment',
            'inventory', 'interfaces', 'mac_table',
            'neighbors', 'power_inline', 'version']

        generated_keys = list(dev.info.keys())

        self.assertTrue(
            all(key in generated_keys
                for key in expected_keys))

        self.assertEqual(dev.info, DeviceOutput.DeviceInfo)

    def test_output_boot(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device,
                          attributes=['info[bootvar][(.*)]'])

        # Get outputs
        dev.maker.outputs[ShowBoot] = {
            '': DeviceOutput.ShowBoot
        }

        # learn the feature
        dev.learn()

        self.assertDictEqual(
            dev.info['bootvar'],
            DeviceOutput.DeviceInfo['bootvar'])

        # asserts that neighbors is the only key in info
        self.assertEqual(
            list(dev.info.keys()),
            ['bootvar'])


if __name__ == '__main__':
    unittest.main()
