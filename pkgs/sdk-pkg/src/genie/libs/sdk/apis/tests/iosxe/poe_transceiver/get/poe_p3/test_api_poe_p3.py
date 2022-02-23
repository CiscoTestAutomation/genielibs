import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.poe_transceiver.get import poe_p3


class TestPoeP3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          A2-9300-3M:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A2-9300-3M']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_poe_p3(self):
        result = poe_p3(self.device)
        expected_output = {'poe_intf': ['TenGigabitEthernet2/0/38', 'TenGigabitEthernet3/0/38'],
 'poe_power_class': ['2', '3'],
 'poe_power_used': [6.0, 6.3]}
        self.assertEqual(result, expected_output)
