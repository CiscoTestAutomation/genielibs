import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_broadband_aaa


class TestConfigureBroadbandAaa(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_ASR1001-X:
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
        self.device = self.testbed.devices['BB_ASR1001-X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_broadband_aaa(self):
        result = configure_broadband_aaa(self.device, 'server_1', 3)
        expected_output = None
        self.assertEqual(result, expected_output)
