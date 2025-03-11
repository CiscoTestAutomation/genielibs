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

def mapper(key, **kwargs):
    return outputs[key]

class test_management(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.submodel = None
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper

    def test_complete_output(self):
        self.maxDiff = None
        m = Management(device=self.device)

        # Learn the feature
        m.learn()

        # Verify Ops was created successfully
        self.assertEqual(m.info, ManagementOutput.ManagementOpsOutput)

    def test_selective_attribute(self):
        self.maxDiff = None
        m = Management(device=self.device)

        # Learn the feature
        m.learn()

        # Check selective attribute
        self.assertEqual('5.4.0.1', m.info['routes']['ipv4']['5.255.253.6/32']['next_hop'])

if __name__ == '__main__':
    unittest.main()
