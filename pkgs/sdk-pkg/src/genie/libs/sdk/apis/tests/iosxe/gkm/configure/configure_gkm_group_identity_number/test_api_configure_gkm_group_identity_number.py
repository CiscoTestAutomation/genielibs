import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gkm.configure import configure_gkm_group_identity_number


class TestConfigureGkmGroupIdentityNumber(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Hub:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: Curie
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_gkm_group_identity_number(self):
        result = configure_gkm_group_identity_number(self.device, 'v4-cust-gdoi1000', '1000')
        expected_output = None
        self.assertEqual(result, expected_output)
