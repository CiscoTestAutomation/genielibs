import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.configure import configure_ptp_priority


class TestConfigurePtpPriority(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24U-NBR2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-24U-NBR2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ptp_priority(self):
        result = configure_ptp_priority(self.device, 20, 128)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ptp_priority_1(self):
        result = configure_ptp_priority(self.device, 29, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ptp_priority_2(self):
        result = configure_ptp_priority(self.device, None, 98)
        expected_output = None
        self.assertEqual(result, expected_output)
