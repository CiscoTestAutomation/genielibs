import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

from genie.libs.ops.management.nxos.management import Management
from genie.libs.ops.management.nxos.tests.management_output import ManagementOutput

# Parser
from genie.libs.parser.nxos.show_routing import ShowIpRoute

outputs = {
    "show ip route vrf management": ManagementOutput.showIPRoute,
}

def mapper(key, **kwargs):
    return outputs[key]

class test_management(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxr')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os"]
        self.device.mapping = {'cli': 'cli'}
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        m = Management(device=self.device)
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        m.learn()

        # Verify Ops was created successfully
        self.assertEqual(m.info, ManagementOutput.ManagementOpsOutput)