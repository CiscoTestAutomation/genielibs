import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_vlan_tag_native


class TestUnconfigVlanTagNative(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_vlan_tag_native(self):
        result = unconfig_vlan_tag_native(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
