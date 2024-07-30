import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.configure import config_qinq_encapsulation_on_interface


class TestConfigQinqEncapsulationOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Kahuna-Sanity:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Kahuna-Sanity']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_qinq_encapsulation_on_interface(self):
        result = config_qinq_encapsulation_on_interface(self.device, '10', '20', 'gigabitethernet 0/0/1.10')
        expected_output = None
        self.assertEqual(result, expected_output)
