import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.verify import verify_rollback_description


class TestVerifyRollbackDescription(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PI-9300-Stack-103:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PI-9300-Stack-103']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_rollback_description(self):
        result = verify_rollback_description(self.device, '1', 'base_label_description')
        expected_output = True
        self.assertEqual(result, expected_output)
