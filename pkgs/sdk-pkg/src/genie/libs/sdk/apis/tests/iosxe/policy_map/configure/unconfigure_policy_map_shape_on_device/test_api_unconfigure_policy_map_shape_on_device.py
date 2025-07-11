import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import unconfigure_policy_map_shape_on_device


class TestUnconfigurePolicyMapShapeOnDevice(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          EPCOT_vijay:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9610
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['EPCOT_vijay']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_policy_map_shape_on_device(self):
        result = unconfigure_policy_map_shape_on_device(self.device, 'llq', 'class-default')
        expected_output = None
        self.assertEqual(result, expected_output)
