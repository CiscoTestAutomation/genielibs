import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.verify import verify_mfib_vrf_hardware_rate


class TestVerifyMfibVrfHardwareRate(unittest.TestCase):

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

    def test_verify_mfib_vrf_hardware_rate(self):
        result = verify_mfib_vrf_hardware_rate(self.device, 'vrf3001', {'228.1.1.1': {'num_of_igmp_groups': 10, 'rate_pps': 10000}}, '30', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
