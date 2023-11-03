import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_parameter_map


class TestConfigureParameterMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_parameter_map(self):
        result = configure_parameter_map(self.device, False, True, 'banner', 'c banner-text c', 'c banner-title c', True, True, True, True, 'html', 'logindevice', None, 'success', True, 10, 'append client-mac tag vis', 11, True, 60, 'consent', 85, True, True, 'vis', '10.10.10.10', '10:10:10::1', '1.1.1.1', '20:20:20::1', 10, True, 'vis', None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
