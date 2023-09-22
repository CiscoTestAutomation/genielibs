import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl


class TestConfigExtendedAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyq-PE1#:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyq-PE1#']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_extended_acl(self):
        result = config_extended_acl(self.device, 'TIME_BASED_ACL_permit', 'permit', 'tcp', 'any', '', '', 'any', '', '', 'telnet', 0, None, 10, '', 'time1', 'eq')
        expected_output = None
        self.assertEqual(result, expected_output)
