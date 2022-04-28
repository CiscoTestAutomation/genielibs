import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_local_pool


class TestConfigureIpLocalPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ASR1002-HX:
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
        self.device = self.testbed.devices['ASR1002-HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_local_pool(self):
        result = configure_ip_local_pool(self.device, 'pool1', '1.1.1.1', '1.1.1.10')
        expected_output = None
        self.assertEqual(result, expected_output)
