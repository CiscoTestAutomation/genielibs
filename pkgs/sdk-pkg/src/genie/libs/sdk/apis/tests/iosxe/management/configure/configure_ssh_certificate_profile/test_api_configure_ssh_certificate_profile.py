import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_ssh_certificate_profile


class TestConfigureSshCertificateProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ssh_certificate_profile(self):
        result = configure_ssh_certificate_profile(self.device, 'CISCO_IDEVID_SUDI', True, True)
        expected_output = None
        self.assertEqual(result, expected_output)
