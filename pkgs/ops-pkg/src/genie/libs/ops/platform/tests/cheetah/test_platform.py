# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie Xbu_shared
from genie.libs.ops.platform.cheetah.ap.platform import Platform
from genie.libs.ops.platform.cheetah.ap.tests.platform_output import PlatformOutput
from genie.libs.parser.cheetah.show_platform import ShowVersion

outputs = {
    'show terminal' : PlatformOutput.showVersion
}

def mapper(key):
    return outputs[key]

class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='cheetah', platform='ap')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os", "platform"]
        self.device.mapping = {'cli': 'cli'}
        mock_connection = Mock()
        mock_connection.device = self.device
        self.device.connectionmgr.connections['cli'] = mock_connection
        mock_connection.execute.side_effect = mapper

    def test_complete_output(self):
        self.maxDiff = None
        f = Platform(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVersion] = \
            {'':PlatformOutput.showVersion}

        # Learn the feature
        f.learn()

        # Verify Ops was created successfully
        self.assertEqual(f.chassis, PlatformOutput.showVersion_ops_output['chassis'])
        self.assertEqual(f.chassis_sn, PlatformOutput.showVersion_ops_output['chassis_sn'])
        self.assertEqual(f.os, PlatformOutput.showVersion_ops_output['os'])
        self.assertEqual(f.version, PlatformOutput.showVersion_ops_output['version'])
        self.assertEqual(f.main_mem, PlatformOutput.showVersion_ops_output['main_mem'])

    def test_empty_parser_output_asr1k(self):
        self.maxDiff = None
        f = Platform(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVersion] = {"": {}}

        # Learn the feature
        f.learn()

        # Check info was not created
        self.assertFalse(hasattr(f, 'version'))

if __name__ == '__main__':
    unittest.main()
