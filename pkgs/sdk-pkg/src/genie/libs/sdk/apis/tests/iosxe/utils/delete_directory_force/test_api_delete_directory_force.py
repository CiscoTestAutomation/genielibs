import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import delete_directory_force


class TestDeleteDirectoryForce(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ACE:
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
        self.device = self.testbed.devices['ACE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_delete_directory_force(self):
        result = delete_directory_force(self.device, 'harddisk', 'Test1', 'Test1', 30)
        expected_output = None
        self.assertEqual(result, expected_output)
