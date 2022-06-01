import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.verify import verify_ptp_profile


class TestVerifyPtpProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          centi_48TX_1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['centi_48TX_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ptp_profile(self):
        result = verify_ptp_profile(self.device, 'ptp mode boundary delay', 15, 5)
        expected_output = False
        self.assertEqual(result, expected_output)
