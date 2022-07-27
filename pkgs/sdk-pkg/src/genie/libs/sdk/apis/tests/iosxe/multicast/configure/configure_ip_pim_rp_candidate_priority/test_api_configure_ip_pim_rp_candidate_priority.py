import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ip_pim_rp_candidate_priority


class TestConfigureIpPimRpCandidatePriority(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          32QC-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['32QC-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_pim_rp_candidate_priority(self):
        result = configure_ip_pim_rp_candidate_priority(self.device, 'Loopback0', 90)
        expected_output = None
        self.assertEqual(result, expected_output)
