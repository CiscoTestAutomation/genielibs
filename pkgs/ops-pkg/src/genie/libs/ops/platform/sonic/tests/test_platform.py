# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie Xbu_shared
from genie.libs.ops.platform.sonic.platform import Platform
from genie.libs.ops.platform.sonic.tests.platform_output import PlatformOutput
from genie.libs.parser.sonic.show_version import ShowVersion
from genie.libs.parser.sonic.show_platform import ShowPlatformInventory


class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='sonic')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os", "platform"]
        self.device.mapping = {'cli': 'cli'}
        mock_connection = Mock()
        mock_connection.device = self.device
        self.device.connectionmgr.connections['cli'] = mock_connection

    def test_complete_output(self):
        self.maxDiff = None
        f = Platform(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}
        
        f.maker.outputs[ShowPlatformInventory] = \
            {'':PlatformOutput.showPlatformInventory}

        # Learn the feature
        f.learn()

        # # Verify Ops was created successfully
        self.assertEqual(f.os, PlatformOutput.showVersion_ops_output['os'])
        self.assertEqual(f.version, PlatformOutput.showVersion_ops_output['version'])
        self.assertEqual(f.chassis_sn, PlatformOutput.showPlatformInventory_ops_output['chassis_sn'])
        self.assertEqual(f.chassis, PlatformOutput.showPlatformInventory_ops_output['chassis'])
        self.assertEqual(f.slot, PlatformOutput.showPlatformInventory_ops_output['slot'])

    def test_empty_parser_output(self):

        self.maxDiff = None
        f = Platform(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVersion] = {"": {}}
        f.maker.outputs[ShowPlatformInventory] = {"": {}}

        # Learn the feature
        f.learn()
        # Check info was not created
        self.assertFalse(hasattr(f, 'version'))

if __name__ == '__main__':
    unittest.main()
