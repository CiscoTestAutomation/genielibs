import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.cheetah.ap.get import get_ip_prefer_mode


class TestGetIpPreferMode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          AP188B.4500.5EE8:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os cheetah --mock_data_dir mock_data --state connect
                protocol: unknown
            os: cheetah
            platform: ap
            type: AP
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AP188B.4500.5EE8']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_ip_prefer_mode(self):
        result = get_ip_prefer_mode(self.device)
        expected_output = 'IPv4'
        self.assertEqual(result, expected_output)
