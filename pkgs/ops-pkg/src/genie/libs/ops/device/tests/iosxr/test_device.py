# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.device.iosxr.device import Device as DeviceModel
from genie.libs.ops.device.tests.iosxr.device_output import DeviceOutput

# Parser
from genie.libs.parser.iosxr.show_cdp import ShowCdpNeighborsDetail
from genie.libs.parser.iosxr.show_lldp import ShowLldpNeighborsDetail
from genie.libs.parser.iosxr.show_interface import ShowInterfaces
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowInventory
from genie.libs.ops.device.device import ShowRunningConfig

outputs = {
    'show cdp neighbors detail': DeviceOutput.ShowCdpNeighborsDetail,
    'show interfaces': DeviceOutput.ShowInterfaces,
    'show inventory': DeviceOutput.ShowInventory,
    'show lldp neighbors detail': DeviceOutput.ShowLldpNeighborsDetail,
    'show running-config': DeviceOutput.ShowRunningConfig,
    'show version': DeviceOutput.ShowVersion
}


def mapper(key, **kwargs):
    return outputs[key]


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxr', platform = 'iosxrv9k')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os"]
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
        dev.maker.outputs[ShowCdpNeighborsDetail] = {'': {}}
        dev.maker.outputs[ShowInterfaces] = {'': {}}
        dev.maker.outputs[ShowInventory] = {'': {}}
        dev.maker.outputs[ShowLldpNeighborsDetail] = {'': {}}
        dev.maker.outputs[ShowRunningConfig] = {'': {}}
        dev.maker.outputs[ShowVersion] = {'': {}}

        dev.learn()

        # Check info was not created
        self.assertFalse(hasattr(dev, 'info'))

    def test_complete_output(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device)

        # Get outputs
        dev.maker.outputs[ShowCdpNeighborsDetail] = {
            '': DeviceOutput.ShowCdpNeighborsDetail}

        dev.maker.outputs[ShowInterfaces] = {
            '': DeviceOutput.ShowInterfaces}

        dev.maker.outputs[ShowInventory] = {
            '': DeviceOutput.ShowInventory}

        dev.maker.outputs[ShowLldpNeighborsDetail] = {
            '': DeviceOutput.ShowLldpNeighborsDetail}

        dev.maker.outputs[ShowVersion] = {
            '': DeviceOutput.ShowVersion}

        dev.maker.outputs[ShowRunningConfig] = {
            '': DeviceOutput.ShowRunningConfig}

        dev.learn()

        expected_keys = [
            'config', 'inventory',
            'interfaces', 'neighbors', 'version']
        generated_keys = list(dev.info.keys())

        self.assertTrue(
            all(key in generated_keys
                for key in expected_keys))

        self.assertEqual(dev.info, DeviceOutput.DeviceInfo)

    def test_output_neighbors(self):
        self.maxDiff = None
        dev = DeviceModel(device=self.device,
                          attributes=['info[neighbors][(.*)]'])

        # Get outputs
        dev.maker.outputs[ShowLldpNeighborsDetail] = {
            '': DeviceOutput.ShowLldpNeighborsDetail
        }
        dev.maker.outputs[ShowCdpNeighborsDetail] = {
            '': DeviceOutput.ShowCdpNeighborsDetail
        }

        # learn the feature
        dev.learn()

        self.assertDictEqual(
            dev.info['neighbors'],
            DeviceOutput.DeviceInfo['neighbors'])

        # asserts that version is the only key in info
        self.assertEqual(
            list(dev.info.keys()),
            ['neighbors'])


if __name__ == '__main__':
    unittest.main()
