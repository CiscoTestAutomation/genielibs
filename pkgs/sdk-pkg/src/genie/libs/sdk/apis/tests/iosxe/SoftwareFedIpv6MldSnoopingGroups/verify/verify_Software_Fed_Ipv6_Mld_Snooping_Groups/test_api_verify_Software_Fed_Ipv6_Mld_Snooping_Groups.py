import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.SoftwareFedIpv6MldSnoopingGroups.verify import verify_Software_Fed_Ipv6_Mld_Snooping_Groups


class TestVerifySoftwareFedIpv6MldSnoopingGroups(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SF1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: '9500'
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SF1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_Software_Fed_Ipv6_Mld_Snooping_Groups(self):
        result = verify_Software_Fed_Ipv6_Mld_Snooping_Groups(self.device, 'active', '20 ff1e::20', 'mem_port', 'TwentyFiveGigE1/0/11')
        expected_output = True
        self.assertEqual(result, expected_output)
