# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

from genie.libs.ops.management.iosxr.management import Management
from genie.libs.ops.management.iosxr.tests.management_output import ManagementOutput

# Parser
from genie.libs.parser.iosxr.show_ipv4 import ShowIpv4VirtualAddressStatus
from genie.libs.parser.iosxr.show_routing import ShowRouteIpv4

outputs = {
    'show ipv4 virtual address status' : ManagementOutput.showIpv4VirtualAddressStatusOutput,
    'show route ipv4 next-hop MgmtEth0/RP0/CPU0/0': ManagementOutput.showRouteIpv4Output
}

def mapper(key):
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

    def test_selective_attribute(self):
        self.maxDiff = None
        m = Management(device=self.device)

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        m.learn()

        # Check selective attribute
        self.assertEqual('5.4.0.1', m.info['routes']['ipv4']['5.255.253.6/32']['next_hop'])

if __name__ == '__main__':
    unittest.main()
