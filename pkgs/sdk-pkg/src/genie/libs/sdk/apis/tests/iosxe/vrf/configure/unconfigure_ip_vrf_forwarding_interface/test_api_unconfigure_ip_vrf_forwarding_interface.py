import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_ip_vrf_forwarding_interface


class TestUnconfigureIpVrfForwardingInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_1HX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_1HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_vrf_forwarding_interface(self):
        result = unconfigure_ip_vrf_forwarding_interface(self.device, 'te0/1/0', 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
