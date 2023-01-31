import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_acl_with_src_dsc_net


class TestUnconfigureAclWithSrcDscNet(unittest.TestCase):

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
            platform: C8000V
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_acl_with_src_dsc_net(self):
        result = unconfigure_acl_with_src_dsc_net(self.device, '100')
        expected_output = None
        self.assertEqual(result, expected_output)
