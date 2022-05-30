import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import verify_ospf_icmp_ping


class TestVerifyOspfIcmpPing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: switch
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ospf_icmp_ping(self):
        result = verify_ospf_icmp_ping(self.device, '131.1.1.1', 100, 0, None, 60, 2, 10, 1400)
        expected_output = True
        self.assertEqual(result, expected_output)
