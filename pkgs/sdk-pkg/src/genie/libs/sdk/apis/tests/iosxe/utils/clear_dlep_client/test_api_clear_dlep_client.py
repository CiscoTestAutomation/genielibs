import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_dlep_client


class TestClearDlepClient(unittest.TestCase):

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
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Kahuna-Sanity']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_dlep_client(self):
        result = clear_dlep_client(self.device, 'GigabitEthernet0/0/4', '132')
        expected_output = None
        self.assertEqual(result, expected_output)
