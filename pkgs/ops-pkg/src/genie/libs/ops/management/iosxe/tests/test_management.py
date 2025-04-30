# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

from genie.libs.ops.management.iosxe.management import Management
from genie.libs.ops.management.iosxe.tests.management_output import ManagementOutput, ManagementOutput2

outputs = {
    "show ip route 0.0.0.0": ManagementOutput.ShowIpRouteDistributor0000Output,
    "show ip route 10.85.84.1": ManagementOutput.ShowIpRouteDistributorIPOutput,
    "show ip interface Ethernet0": ManagementOutput.ShowIpInterfaceEthernet0Output,
}


class test_management(unittest.TestCase):

    def setUp(self):
        self.device = Device(name="aDevice")
        self.device.os = "iosxe"
        self.device.custom["abstraction"] = {"order": ["os"]}
        self.device.mapping = {}
        self.device.mapping["cli"] = "cli"
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections["cli"] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = lambda key, timeout=None: outputs[key]

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
        self.assertEqual("10.85.84.48/24", m.info["management"]["ipv4_address"])


outputs2 = {
    "show ip route 0.0.0.0": ManagementOutput2.ShowIpRouteDistributor0000Output,
    "show ip route 172.27.147.1": ManagementOutput2.ShowIpRouteDistributorIPOutput,
    "show ip arp 172.27.147.1": ManagementOutput2.ShowIpArpIPOutput,
    "show ip interface Ethernet0/0": ManagementOutput2.ShowIpInterfaceIfnameOutput,
}


class test_management2(unittest.TestCase):

    def setUp(self):
        self.device = Device(name="aDevice")
        self.device.os = "ios"
        self.device.custom["abstraction"] = {"order": ["os"]}
        self.device.mapping = {}
        self.device.mapping["cli"] = "cli"
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections["cli"] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = lambda key, timeout=None: outputs2[key]

    def test_complete_output(self):
        self.maxDiff = None
        m = Management(device=self.device)

        # Learn the feature
        m.learn()

        # Verify Ops was created successfully
        self.assertEqual(m.info, ManagementOutput2.ManagementOpsOutput)


if __name__ == "__main__":
    unittest.main()
