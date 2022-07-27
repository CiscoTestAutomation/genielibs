import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_acl


class TestUnconfigureAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: csr1000v
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_acl(self):
        result = unconfigure_acl(self.device, 40, True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_acl_1(self):
        result = unconfigure_acl(self.device, 40, False)
        expected_output = None
        self.assertEqual(result, expected_output)
