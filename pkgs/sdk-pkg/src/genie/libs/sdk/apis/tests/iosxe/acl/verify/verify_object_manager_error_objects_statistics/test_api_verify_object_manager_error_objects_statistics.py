import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.verify import verify_object_manager_error_objects_statistics


class TestVerifyObjectManagerErrorObjectsStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: c9600
            custom:
              abstraction:
                order: [os, platform]
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_object_manager_error_objects_statistics(self):
        result = verify_object_manager_error_objects_statistics(self.device, 'fp active', 1)
        expected_output = False
        self.assertEqual(result, expected_output)
