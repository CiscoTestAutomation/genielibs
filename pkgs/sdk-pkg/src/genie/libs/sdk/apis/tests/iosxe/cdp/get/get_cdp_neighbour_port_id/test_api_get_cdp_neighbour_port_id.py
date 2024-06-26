import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.get import get_cdp_neighbour_port_id


class TestGetCdpNeighbourPortId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-HMS4EG8CGR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3300
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-HMS4EG8CGR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_cdp_neighbour_port_id(self):
        result = get_cdp_neighbour_port_id(self.device, 'GigabitEthernet1/6')
        expected_output = ['GigabitEthernet1/6']
        self.assertEqual(result, expected_output)
