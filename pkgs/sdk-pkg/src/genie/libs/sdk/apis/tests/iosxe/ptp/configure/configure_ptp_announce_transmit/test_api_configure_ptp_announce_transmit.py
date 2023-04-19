import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.configure import configure_ptp_announce_transmit


class TestConfigurePtpAnnounceTransmit(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          CE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ptp_announce_transmit(self):
        result = configure_ptp_announce_transmit(self.device, 'HundredGigE1/0/48')
        expected_output = None
        self.assertEqual(result, expected_output)
