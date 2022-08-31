import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_running_config


class TestGetInterfaceRunningConfig(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: csr1000v
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_running_config(self):
        result = get_interface_running_config(self.device, "GigabitEthernet1")
        expected_output = {
            "Building configuration...": {},
            "Current configuration : 135 bytes": {},
            "end": {},
            "interface GigabitEthernet1": {
                "ip address dhcp": {},
                "negotiation auto": {},
                "no mop enabled": {},
                "no mop sysid": {},
                "shutdown": {},
                "vrf forwarding Mgmt-intf": {},
            },
        }
        self.assertEqual(result, expected_output)
