import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.igmp.verify import verify_igmp_groups_under_vrf


class TestVerifyIgmpGroupsUnderVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_igmp_groups_under_vrf(self):
        result = verify_igmp_groups_under_vrf(self.device, 'vrf3001', [['232.1.1.1', '0.0.0.0'], ['228.1.1.1', '121.1.1.2']], 10, 'vlan3001', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
