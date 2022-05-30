import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_ip_traffic


class TestClearIpTraffic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr1:
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
        self.device = self.testbed.devices['kparames_csr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ip_traffic(self):
        result = clear_ip_traffic(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
