import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.verify import verify_mpls_forwarding_table_vrf_mdt


class TestVerifyMplsForwardingTableVrfMdt(unittest.TestCase):

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

    def test_verify_mpls_forwarding_table_vrf_mdt(self):
        result = verify_mpls_forwarding_table_vrf_mdt(self.device, 'vrf3001', 'mdt', '3001:1', '500000', 1, 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
