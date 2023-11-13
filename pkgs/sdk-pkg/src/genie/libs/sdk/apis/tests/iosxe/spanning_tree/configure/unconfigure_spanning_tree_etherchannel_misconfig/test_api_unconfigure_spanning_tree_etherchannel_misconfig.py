import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import unconfigure_spanning_tree_etherchannel_misconfig


class TestUnconfigureSpanningTreeEtherchannelMisconfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          l2sec_clarke_2006:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: switch
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['l2sec_clarke_2006']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_spanning_tree_etherchannel_misconfig(self):
        result = unconfigure_spanning_tree_etherchannel_misconfig(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
