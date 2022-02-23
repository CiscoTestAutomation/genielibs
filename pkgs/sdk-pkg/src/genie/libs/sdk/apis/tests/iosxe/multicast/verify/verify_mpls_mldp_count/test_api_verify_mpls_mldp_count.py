import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.verify import verify_mpls_mldp_count


class TestVerifyMplsMldpCount(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          C9400-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9400-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_mpls_mldp_count(self):
        result = verify_mpls_mldp_count(self.device, 1, 0, 1, 1, 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
