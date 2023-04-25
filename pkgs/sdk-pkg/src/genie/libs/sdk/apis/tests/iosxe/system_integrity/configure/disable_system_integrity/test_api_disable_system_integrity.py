import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.system_integrity.configure import disable_system_integrity


class TestDisableSystemIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          pi-infra8:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['pi-infra8']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_disable_system_integrity(self):
        result = disable_system_integrity(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
