import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_names


class TestGetInterfaceNames(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["R1_xe"]
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_names(self):
        result = get_interface_names(self.device)
        expected_output = [
            "GigabitEthernet1",
            "GigabitEthernet2",
            "GigabitEthernet2.90",
            "GigabitEthernet2.110",
            "GigabitEthernet2.115",
            "GigabitEthernet2.120",
            "GigabitEthernet2.390",
            "GigabitEthernet2.410",
            "GigabitEthernet2.415",
            "GigabitEthernet2.420",
            "GigabitEthernet3",
            "GigabitEthernet3.90",
            "GigabitEthernet3.110",
            "GigabitEthernet3.115",
            "GigabitEthernet3.120",
            "GigabitEthernet3.390",
            "GigabitEthernet3.410",
            "GigabitEthernet3.415",
            "GigabitEthernet3.420",
            "GigabitEthernet4",
            "GigabitEthernet5",
            "GigabitEthernet6",
            "GigabitEthernet7",
            "Loopback0",
            "Loopback300",
            "Port-channel12",
            "Port-channel13",
            "Tunnel0",
            "Tunnel1",
            "Tunnel2",
            "Tunnel3",
            "Tunnel4",
            "Tunnel5",
            "Tunnel6",
            "Tunnel7",
            "Tunnel8",
            "Tunnel9",
        ]
        self.assertEqual(result, expected_output)
