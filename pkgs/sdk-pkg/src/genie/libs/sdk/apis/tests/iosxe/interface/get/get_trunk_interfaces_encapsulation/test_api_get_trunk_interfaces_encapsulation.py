import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_trunk_interfaces_encapsulation


class TestGetTrunkInterfacesEncapsulation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_trunk_interfaces_encapsulation(self):
        result = get_trunk_interfaces_encapsulation(device=self.device, interfaces=['TenGigabitEthernet1/0/1'])
        expected_output = {'TenGigabitEthernet1/0/1': '802.1q'}
        self.assertEqual(result, expected_output)
