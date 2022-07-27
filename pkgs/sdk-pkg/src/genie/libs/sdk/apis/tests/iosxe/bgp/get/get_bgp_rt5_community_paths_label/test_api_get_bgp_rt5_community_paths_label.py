import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_rt5_community_paths_label


class TestGetBgpRt5CommunityPathsLabel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CGW-laas-c9500-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat
            type: cat
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CGW-laas-c9500-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_bgp_rt5_community_paths_label(self):
        result = get_bgp_rt5_community_paths_label(self.device, 'l2vpn evpn', '0', '20.101.1.3', '32', '101')
        expected_output = {'ext_community': ['RT:300:3000101'],
 'paths': '1 available, best #1, table evi_101, re-originated from '
          '[2][30.0.1.11:101][0][48][005056840448][32][20.101.1.3]/24',
 'vni_labels': ['3000101']}
        self.assertEqual(result, expected_output)
