import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_nsf_xfsu


class TestConfigureIsisNsfXfsu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300stack:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300stack']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_isis_nsf_xfsu(self):
        result = configure_isis_nsf_xfsu(self.device, '49.1290.0000.0014.00', '1', 'loopback0', 'wide', 'ietf', 'connected')
        expected_output = None
        self.assertEqual(result, expected_output)
