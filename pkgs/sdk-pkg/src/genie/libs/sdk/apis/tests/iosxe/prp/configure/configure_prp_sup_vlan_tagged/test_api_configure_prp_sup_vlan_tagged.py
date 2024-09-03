import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.prp.configure import configure_prp_sup_vlan_tagged


class TestConfigurePrpSupVlanTagged(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PRP-A:
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
        self.device = self.testbed.devices['PRP-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_prp_sup_vlan_tagged(self):
        result = configure_prp_sup_vlan_tagged(self.device, 1)
        expected_output = None
        self.assertEqual(result, expected_output)
