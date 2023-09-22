import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gdoi.configure import configure_gdoi_group


class TestConfigureGdoiGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          KS1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8300-1N1S-4T2X
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['KS1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_gdoi_group(self):
        result = configure_gdoi_group(self.device, 'SUITEBv4', False, 9000, '15.15.15.1', True, 'aes 256', '14000', '10', '3', 'REKEYRSA', False, '10', 'SUITEBgcm128', 'SUITEBv4acl', None, False, '20', False, '15.15.15.1', False, '245', '16.16.16.1', True, None, 1, 'IKEV2-PROF1', 121, 'IKEV2-PROF1', True)
        expected_output = None
        self.assertEqual(result, expected_output)
