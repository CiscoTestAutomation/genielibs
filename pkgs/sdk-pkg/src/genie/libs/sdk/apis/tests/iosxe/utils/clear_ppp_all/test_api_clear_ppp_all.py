import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_ppp_all


class TestClearPppAll(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          RM:
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
        self.device = self.testbed.devices['RM']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ppp_all(self):
        result = clear_ppp_all(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
