import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.configure import configure_ptp_vlan


class TestConfigurePtpVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9400-LaaS:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9400
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400-LaaS']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ptp_vlan(self):
        result = configure_ptp_vlan(self.device, 'GigabitEthernet1/1/0/1', '101')
        expected_output = None
        self.assertEqual(result, expected_output)
