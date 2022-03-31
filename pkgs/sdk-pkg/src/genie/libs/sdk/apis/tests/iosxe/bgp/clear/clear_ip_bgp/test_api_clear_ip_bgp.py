import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.clear import clear_ip_bgp


class TestClearIpBgp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          a2_acc_9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['a2_acc_9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ip_bgp(self):
        result = clear_ip_bgp(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
