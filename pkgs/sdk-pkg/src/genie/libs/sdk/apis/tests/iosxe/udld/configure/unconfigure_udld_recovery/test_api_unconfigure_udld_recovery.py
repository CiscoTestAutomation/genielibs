import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.udld.configure import unconfigure_udld_recovery


class TestUnconfigureUdldRecovery(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9200_access:
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
        self.device = self.testbed.devices['9200_access']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_udld_recovery(self):
        result = unconfigure_udld_recovery(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
