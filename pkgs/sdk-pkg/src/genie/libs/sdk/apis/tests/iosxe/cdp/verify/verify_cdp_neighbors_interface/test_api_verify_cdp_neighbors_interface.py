import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.verify import verify_cdp_neighbors_interface


class TestVerifyCdpNeighborsInterface(unittest.TestCase):

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

    def test_verify_cdp_neighbors_interface(self):
        result = verify_cdp_neighbors_interface(self.device, ['GigabitEthernet1/6'], ['Gig 1/6'], 60, 10)
        expected_output = False
        self.assertEqual(result, expected_output)
