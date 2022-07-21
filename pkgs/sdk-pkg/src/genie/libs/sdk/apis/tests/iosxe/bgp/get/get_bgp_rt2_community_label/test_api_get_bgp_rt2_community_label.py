import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_rt2_community_label


class TestGetBgpRt2CommunityLabel(unittest.TestCase):

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

    def test_get_bgp_rt2_community_label(self):
        result = get_bgp_rt2_community_label(self.device, 'l2vpn evpn', '0', '000011112222', '20.101.1.254', '101')
        expected_output = {'ext_community': ['RT:300:2000101', 'RT:300:3000101', 'ENCAP:8'],
 'labels': ['2000101']}
        self.assertEqual(result, expected_output)
