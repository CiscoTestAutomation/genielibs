import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gdoi.configure import configure_gdoi_group


class TestConfigureGdoiGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          INT1:
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
        self.device = self.testbed.devices['INT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_gdoi_group(self):
        result = configure_gdoi_group(self.device, 'bw6000', False, '6000', None, 'True', 'aes 256', '14000', '10', '3', 'REKEYRSA', 'False', '10', 'bw600', 'bw600-crypto-policy', None, False, '20', 'False', '192.168.2.1', 'True', '245', '123.141.2.3', False, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
