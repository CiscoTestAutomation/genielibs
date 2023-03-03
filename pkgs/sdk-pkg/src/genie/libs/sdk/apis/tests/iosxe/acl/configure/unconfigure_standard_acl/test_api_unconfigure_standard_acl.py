import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_standard_acl


class TestUnconfigureStandardAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_standard_acl(self):
        result = unconfigure_standard_acl(self.device, 'Test5', '20', 'permit', 'host', '232.1.2.10')
        expected_output = None
        self.assertEqual(result, expected_output)
