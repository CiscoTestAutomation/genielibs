import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.verify import verify_mpls_summary_lspa


class TestVerifyMplsSummaryLspa(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_mpls_summary_lspa(self):
        result = verify_mpls_summary_lspa(self.device, 1)
        expected_output = '1'
        self.assertEqual(result, expected_output)
