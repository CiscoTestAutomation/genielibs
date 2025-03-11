# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

from genie.libs.ops.management.iosxe.management import Management
from genie.libs.ops.management.iosxe.tests.management_output import ManagementOutput

outputs = {
    "show ip route 0.0.0.0": ManagementOutput.ShowIpRouteDistributor0000Output,
    "show ip route 10.85.84.1": ManagementOutput.ShowIpRouteDistributorIPOutput,
    "show ip interface Ethernet0": ManagementOutput.ShowIpInterfaceEthernet0Output,
}

def mapper(key, **kwargs):
    return outputs[key]

class test_management(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
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
        self.assertEqual('10.85.84.48/24', m.info['management']['ipv4_address'])

if __name__ == '__main__':
    unittest.main()
